const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ROOT_DIR = 'c:\\Users\\Ali Raza Bhatti\\Desktop\\AuraToolKit 360';
const PORT = 8092;

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
        '--remote-debugging-port=9244',
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
            const res = await fetch('http://127.0.0.1:9244/json/version');
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
    const targetWsUrl = `ws://127.0.0.1:9244/devtools/page/${targetId}`;
    const pageCdp = new CDPClient(targetWsUrl);
    await pageCdp.connect();

    await pageCdp.send('Page.enable');
    await pageCdp.send('DOM.enable');

    const results = [];

    // --- TEST 1: /ilovepdf-alternative/ ---
    console.log('\n--- Testing /ilovepdf-alternative/ ---');
    await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/ilovepdf-alternative/` });
    await new Promise(r => setTimeout(r, 1200));

    let evalRes = await pageCdp.send('Runtime.evaluate', {
        expression: `({
            title: document.title,
            h1: document.querySelector('h1') ? document.querySelector('h1').innerText : null,
            tableRows: document.querySelectorAll('.compare-table tbody tr').length,
            faqCards: document.querySelectorAll('.faq-card').length,
            toolsCount: document.querySelectorAll('.tool-card-launch').length,
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth
        })`,
        returnByValue: true
    });
    console.log('iLovePDF Alternative data:', JSON.stringify(evalRes.result.value, null, 2));
    results.push({
        page: '/ilovepdf-alternative/',
        pass: evalRes.result.value.tableRows > 4 && evalRes.result.value.toolsCount >= 6 && evalRes.result.value.faqCards >= 5
    });

    // --- TEST 2: /canva-resume-alternative/ ---
    console.log('\n--- Testing /canva-resume-alternative/ ---');
    await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/canva-resume-alternative/` });
    await new Promise(r => setTimeout(r, 1200));

    evalRes = await pageCdp.send('Runtime.evaluate', {
        expression: `({
            title: document.title,
            h1: document.querySelector('h1') ? document.querySelector('h1').innerText : null,
            tableRows: document.querySelectorAll('.compare-table tbody tr').length,
            reasonsCount: document.querySelectorAll('.reason-card').length,
            realityCards: document.querySelectorAll('.reality-card').length,
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth
        })`,
        returnByValue: true
    });
    console.log('Canva Alternative data:', JSON.stringify(evalRes.result.value, null, 2));
    results.push({
        page: '/canva-resume-alternative/',
        pass: evalRes.result.value.tableRows > 4 && evalRes.result.value.reasonsCount === 5 && evalRes.result.value.realityCards === 2
    });

    // --- TEST 3: /converter/resize-signature/ ---
    console.log('\n--- Testing /converter/resize-signature/ ---');
    await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/converter/resize-signature/` });
    await new Promise(r => setTimeout(r, 1200));

    evalRes = await pageCdp.send('Runtime.evaluate', {
        expression: `(async () => {
            window.alert = function(msg) { console.log('Suppressed alert:', msg); };
            const h1 = document.querySelector('h1').innerText;
            const presets = document.getElementById('sigPresetSelect').options.length;
            const targetKbs = document.getElementById('sigTargetKb').options.length;
            
            // Create a fake test signature image (black text on white canvas)
            const testCanvas = document.createElement('canvas');
            testCanvas.width = 400;
            testCanvas.height = 150;
            const tctx = testCanvas.getContext('2d');
            tctx.fillStyle = '#ffffff';
            tctx.fillRect(0, 0, 400, 150);
            tctx.fillStyle = '#000000';
            tctx.font = '30px cursive';
            tctx.fillText('John Doe Specimen', 50, 80);

            // Load into rawSignatureImg
            const img = new Image();
            await new Promise(res => {
                img.onload = res;
                img.src = testCanvas.toDataURL('image/png');
            });
            rawSignatureImg = img;

            // Trigger processSignature
            processSignature();

            const preview = document.getElementById('previewCanvas');
            const badge = document.getElementById('resultBadge').innerText;
            const dl = document.getElementById('downloadBtn').href;

            return {
                h1,
                presets,
                targetKbs,
                previewWidth: preview.width,
                previewHeight: preview.height,
                badge,
                hasDownload: dl.startsWith('data:image/jpeg')
            };
        })()`,
        awaitPromise: true,
        returnByValue: true
    });
    console.log('Resize Signature data:', JSON.stringify(evalRes.result.value, null, 2));
    results.push({
        page: '/converter/resize-signature/',
        pass: evalRes.result.value.previewWidth === 140 && evalRes.result.value.previewHeight === 60 && evalRes.result.value.hasDownload
    });

    // --- TEST 4: /resume-score-checker/ ATS Scorecard Canvas ---
    console.log('\n--- Testing /resume-score-checker/ ATS Scorecard Badge ---');
    await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/resume-score-checker/` });
    await new Promise(r => setTimeout(r, 1200));

    evalRes = await pageCdp.send('Runtime.evaluate', {
        expression: `(() => {
            // Trigger test render
            renderResults({
                isStandalone: false,
                score: 92,
                grade: 'A+',
                density: 16,
                filename: 'Sarah_Connor_Lead_Dev.pdf',
                matched: ['python', 'aws', 'docker', 'react', 'kubernetes', 'typescript'],
                missing: ['graphql'],
                total: 7
            });

            const canvas = document.getElementById('scorecardCanvas');
            const dataUrl = canvas.toDataURL('image/png');

            return {
                canvasWidth: canvas.width,
                canvasHeight: canvas.height,
                dataUrlLength: dataUrl.length,
                isDataUrlValid: dataUrl.startsWith('data:image/png;base64,'),
                cardDisplayed: document.getElementById('resultCard').style.display !== 'none',
                scorecardSectionExists: !!document.getElementById('scorecardSection')
            };
        })()`,
        returnByValue: true
    });
    console.log('Scorecard Verification data:', JSON.stringify(evalRes.result.value, null, 2));
    results.push({
        page: '/resume-score-checker/ scorecard',
        pass: evalRes.result.value.canvasWidth === 1200 && evalRes.result.value.canvasHeight === 630 && evalRes.result.value.dataUrlLength > 20000
    });

    // Take screenshot of Scorecard
    const ss = await pageCdp.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ROOT_DIR, 'scratch', 'scorecard_test_shot.png'), Buffer.from(ss.data, 'base64'));
    console.log('Saved screenshot to scratch/scorecard_test_shot.png');

    // Mobile viewport overflow check (375px)
    console.log('\n--- Mobile Viewport (375px) Overflow Check ---');
    await pageCdp.send('Emulation.setDeviceMetricsOverride', {
        width: 375,
        height: 667,
        deviceScaleFactor: 2,
        mobile: true
    });

    for (const testUrl of ['/ilovepdf-alternative/', '/canva-resume-alternative/', '/converter/resize-signature/']) {
        await pageCdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}${testUrl}` });
        await new Promise(r => setTimeout(r, 800));
        const overflowCheck = await pageCdp.send('Runtime.evaluate', {
            expression: `({
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                hasHorizontalScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth
            })`,
            returnByValue: true
        });
        console.log(`Mobile 375px ${testUrl}:`, overflowCheck.result.value);
        results.push({
            page: `Mobile 375px ${testUrl}`,
            pass: !overflowCheck.result.value.hasHorizontalScroll
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
        console.log(`${r.pass ? '✅ PASS' : '❌ FAIL'}: ${r.page}`);
        if (!r.pass) allPassed = false;
    });
    console.log('Overall Status:', allPassed ? '🎉 ALL TESTS PASSED!' : '❌ SOME TESTS FAILED');
    process.exit(allPassed ? 0 : 1);
}

runTests().catch(err => {
    console.error('Fatal error in tests:', err);
    process.exit(1);
});
