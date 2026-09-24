const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ROOT_DIR = 'c:\\Users\\Ali Raza Bhatti\\Desktop\\AuraToolKit 360';
const PORT = 8095;
const CDP_PORT = 9245;

function startServer() {
    return new Promise(resolve => {
        const mime = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.svg': 'image/svg+xml'
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
                res.end('404');
            }
        });
        server.listen(PORT, '127.0.0.1', () => resolve(server));
    });
}

function launchChrome() {
    return spawn(CHROME_PATH, [
        '--headless=new',
        `--remote-debugging-port=${CDP_PORT}`,
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
            const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/version`);
            const data = await res.json();
            return data.webSocketDebuggerUrl;
        } catch (e) {
            await new Promise(r => setTimeout(r, 200));
        }
    }
    throw new Error('Chrome CDP connection timed out');
}

async function run() {
    const server = await startServer();
    const chromeProc = launchChrome();
    
    try {
        const wsUrl = await getDebuggerUrl();
        const client = new CDPClient(wsUrl);
        await client.connect();

        const { targetId } = await client.send('Target.createTarget', { url: 'about:blank' });
        const targetWsUrl = `ws://127.0.0.1:${CDP_PORT}/devtools/page/${targetId}`;
        const pageClient = new CDPClient(targetWsUrl);
        await pageClient.connect();

        await pageClient.send('Page.enable');
        await pageClient.send('DOM.enable');
        await pageClient.send('Emulation.setDeviceMetricsOverride', {
            width: 375,
            height: 812,
            deviceScaleFactor: 2,
            mobile: true
        });

        await pageClient.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/resume-cv-maker/` });
        await new Promise(r => setTimeout(r, 2500));

        const evalResult = await pageClient.send('Runtime.evaluate', {
            expression: `(() => {
                const formCol = document.getElementById('resumeFormCol');
                if (!formCol) return { error: 'no formCol' };
                
                const overflowing = [];
                const all = formCol.querySelectorAll('*');
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    const comp = window.getComputedStyle(el);
                    if (rect.width > 350 || el.scrollWidth > 350) {
                        overflowing.push({
                            tag: el.tagName,
                            id: el.id,
                            className: el.className,
                            html: el.outerHTML.substring(0, 100),
                            rectWidth: Math.round(rect.width),
                            scrollWidth: el.scrollWidth,
                            minWidth: comp.minWidth,
                            width: comp.width
                        });
                    }
                }
                return overflowing;
            })()`,
            returnByValue: true
        });

        console.log("OVERFLOWING INSIDE FORM COL:");
        console.log(JSON.stringify(evalResult.result.value, null, 2));

        pageClient.close();
        client.close();
    } finally {
        chromeProc.kill();
        server.close();
    }
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});
