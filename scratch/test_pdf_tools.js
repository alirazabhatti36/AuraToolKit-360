const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ROOT_DIR = 'c:\\Users\\Ali Raza Bhatti\\Desktop\\AuraToolKit 360';
const PORT = 8093;

function startServer() {
    return new Promise(resolve => {
        const mime = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.svg': 'image/svg+xml',
            '.jpg': 'image/jpeg'
        };
        const server = http.createServer((req, res) => {
            let p = req.url.split('?')[0];
            if (p.endsWith('/')) p += 'index.html';
            let fp = path.join(ROOT_DIR, p);
            if (!fs.existsSync(fp) && fs.existsSync(fp + '.html')) fp += '.html';
            if (fs.existsSync(fp) && fs.statSync(fp).isFile()) {
                res.writeHead(200, { 'Content-Type': mime[path.extname(fp)] || 'text/plain' });
                fs.createReadStream(fp).pipe(res);
            } else {
                res.writeHead(404);
                res.end('404 Not Found: ' + p);
            }
        });
        server.listen(PORT, '127.0.0.1', () => resolve(server));
    });
}

function launchChrome() {
    return spawn(CHROME_PATH, [
        '--headless=new',
        '--remote-debugging-port=9245',
        '--disable-gpu',
        '--no-sandbox'
    ]);
}

class CDPClient {
    constructor(wsUrl) {
        this.wsUrl = wsUrl;
        this.msgId = 0;
        this.callbacks = new Map();
    }
    connect() {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(this.wsUrl);
            this.ws.onopen = resolve;
            this.ws.onerror = reject;
            this.ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                if (data.id && this.callbacks.has(data.id)) {
                    const cb = this.callbacks.get(data.id);
                    this.callbacks.delete(data.id);
                    if (data.error) cb.reject(data.error);
                    else cb.resolve(data.result);
                }
            };
        });
    }
    send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const id = ++this.msgId;
            this.callbacks.set(id, { resolve, reject });
            this.ws.send(JSON.stringify({ id, method, params }));
        });
    }
    close() {
        if (this.ws) this.ws.close();
    }
}

async function getDebuggerUrl() {
    for (let i = 0; i < 30; i++) {
        try {
            const res = await fetch('http://127.0.0.1:9245/json/version');
            const data = await res.json();
            return data.webSocketDebuggerUrl;
        } catch (e) {
            await new Promise(r => setTimeout(r, 200));
        }
    }
    throw new Error('Could not connect to Chrome debugging port');
}

async function runTests() {
    console.log('1. Starting HTTP server on port ' + PORT + '...');
    const server = await startServer();

    console.log('2. Launching headless Chrome...');
    const chrome = launchChrome();
    const wsUrl = await getDebuggerUrl();
    const cdp = new CDPClient(wsUrl);
    await cdp.connect();

    const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
    const targetWsUrl = `ws://127.0.0.1:9245/devtools/page/${targetId}`;
    const pageCdp = new CDPClient(targetWsUrl);
    await pageCdp.connect();

    await pageCdp.send('Page.enable');
    await pageCdp.send('DOM.enable');

    const results = [];
    const tools = [
        { path: '/converter/pdf-to-word/', action: '/pdf-to-word' },
        { path: '/converter/compress-pdf/', action: '/compress-pdf' },
        { path: '/converter/merge-pdf/', action: '/merge-pdf' }
    ];

    for (const tool of tools) {
        console.log(`\n--- Testing ${tool.path} ---`);
        await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}${tool.path}` });
        await new Promise(r => setTimeout(r, 1000));

        const data = await pageCdp.send('Runtime.evaluate', {
            expression: `(() => {
                const h1 = document.querySelector('h1') ? document.querySelector('h1').innerText : null;
                const schema = document.querySelector('script[type="application/ld+json"]');
                let parsedSchema = null;
                try { parsedSchema = JSON.parse(schema.textContent); } catch(e) {}
                
                const form = document.querySelector('form[data-action="${tool.action}"]');
                const fileInput = form ? form.querySelector('input[type="file"]') : null;
                const submitBtn = form ? form.querySelector('button[type="submit"]') : null;

                return {
                    title: document.title,
                    h1,
                    hasSchema: !!parsedSchema && !!parsedSchema['@graph'],
                    graphTypes: parsedSchema && parsedSchema['@graph'] ? parsedSchema['@graph'].map(g => g['@type']) : [],
                    hasForm: !!form,
                    hasFileInput: !!fileInput,
                    hasSubmitBtn: !!submitBtn,
                    scrollWidth: document.documentElement.scrollWidth,
                    clientWidth: document.documentElement.clientWidth
                };
            })()`,
            returnByValue: true
        });

        console.log(`${tool.path} evaluation:`, JSON.stringify(data.result.value, null, 2));
        results.push({
            tool: tool.path,
            pass: data.result.value.h1 && data.result.value.hasSchema && data.result.value.hasForm
        });
    }

    // Mobile check (375px)
    console.log('\n--- Mobile Viewport (375px) Overflow Check ---');
    await pageCdp.send('Emulation.setDeviceMetricsOverride', {
        width: 375,
        height: 667,
        deviceScaleFactor: 2,
        mobile: true
    });

    for (const tool of tools) {
        await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}${tool.path}` });
        await new Promise(r => setTimeout(r, 800));
        const overflow = await pageCdp.send('Runtime.evaluate', {
            expression: `({
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                hasHorizontalScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth
            })`,
            returnByValue: true
        });
        console.log(`Mobile 375px ${tool.path}:`, overflow.result.value);
        results.push({
            tool: `Mobile 375px ${tool.path}`,
            pass: !overflow.result.value.hasHorizontalScroll
        });
    }

    // Teardown
    pageCdp.close();
    cdp.close();
    chrome.kill();
    server.close();

    console.log('\n================ TEST SUMMARY ================');
    let allPassed = true;
    results.forEach(r => {
        console.log(`${r.pass ? '✅ PASS' : '❌ FAIL'}: ${r.tool}`);
        if (!r.pass) allPassed = false;
    });
    console.log('Overall Status:', allPassed ? '🎉 ALL TESTS PASSED!' : '❌ SOME TESTS FAILED');
    process.exit(allPassed ? 0 : 1);
}

runTests().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
