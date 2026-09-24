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
        await new Promise(r => setTimeout(r, 1200));

        // Inject complete mobile optimization CSS
        await pageClient.send('Runtime.evaluate', {
            expression: `(() => {
                const style = document.createElement('style');
                style.id = 'complete-mobile-fix';
                style.textContent = \`
                    html, body {
                        overflow-x: hidden !important;
                        max-width: 100vw !important;
                        width: 100% !important;
                        position: relative;
                    }
                    .ambient-glow-top-left, .ambient-glow-top-right, .ambient-glow-mid {
                        display: none !important;
                    }
                    .navbar {
                        padding: 0.75rem 0.9rem !important;
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    .nav-container {
                        width: 100% !important;
                        max-width: 100% !important;
                        gap: 0.5rem !important;
                        box-sizing: border-box !important;
                    }
                    .nav-right-actions {
                        gap: 0.4rem !important;
                    }
                    .container {
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        padding: 1rem 0.8rem 5.5rem !important;
                        box-sizing: border-box !important;
                    }
                    .template-top-card {
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        padding: 1rem 0.85rem !important;
                        border-radius: 16px !important;
                        box-sizing: border-box !important;
                    }
                    .template-grid {
                        display: flex !important;
                        overflow-x: auto !important;
                        -webkit-overflow-scrolling: touch;
                        scroll-snap-type: x mandatory;
                        gap: 0.65rem !important;
                        padding-bottom: 0.6rem !important;
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        box-sizing: border-box !important;
                    }
                    .template-chip {
                        min-width: 130px !important;
                        max-width: 130px !important;
                        flex: 0 0 130px !important;
                        scroll-snap-align: start;
                        padding: 0.55rem !important;
                        min-height: 84px !important;
                        box-sizing: border-box !important;
                    }
                    .customizer-toolbar {
                        display: flex !important;
                        flex-direction: column !important;
                        gap: 0.85rem !important;
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        box-sizing: border-box !important;
                    }
                    .customizer-group {
                        width: 100% !important;
                        max-width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    .segmented-control {
                        width: 100% !important;
                        display: flex !important;
                        box-sizing: border-box !important;
                    }
                    .seg-btn {
                        flex: 1 !important;
                        text-align: center !important;
                        padding: 0.45rem 0.2rem !important;
                        font-size: 0.76rem !important;
                    }
                    .page-setup-toolbar {
                        display: flex !important;
                        flex-direction: column !important;
                        align-items: stretch !important;
                        gap: 0.85rem !important;
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        box-sizing: border-box !important;
                    }
                    .layout {
                        display: block !important;
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        box-sizing: border-box !important;
                    }
                    .card {
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        padding: 1.1rem 0.9rem !important;
                        border-radius: 16px !important;
                        box-sizing: border-box !important;
                    }
                    .section-head, .entry-head {
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    .field input, .field textarea, .field select {
                        width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    .photo-picker {
                        width: 100% !important;
                        max-width: 100% !important;
                        box-sizing: border-box !important;
                    }
                    .info-section, .info-card, .features-grid, .footer-inner {
                        width: 100% !important;
                        max-width: 100% !important;
                        min-width: 0 !important;
                        box-sizing: border-box !important;
                    }
                    .features-grid {
                        grid-template-columns: 1fr !important;
                    }
                    .footer-inner {
                        grid-template-columns: 1fr !important;
                        padding: 2rem 1rem !important;
                    }
                \`;
                document.head.appendChild(style);
            })()`
        });

        await new Promise(r => setTimeout(r, 600));

        const evalResult = await pageClient.send('Runtime.evaluate', {
            expression: `(() => {
                const vw = window.innerWidth;
                const docWidth = document.documentElement.scrollWidth;
                const bodyWidth = document.body.scrollWidth;

                const overflowing = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    // exclude horizontally scrolling children
                    if (el.closest('.template-grid') || el.closest('.preview-scroll-wrapper')) continue;
                    if (rect.right > vw + 0.5) {
                        overflowing.push({
                            tag: el.tagName,
                            id: el.id,
                            className: el.className,
                            rectRight: Math.round(rect.right),
                            rectWidth: Math.round(rect.width)
                        });
                    }
                }

                return {
                    vw,
                    docWidth,
                    bodyWidth,
                    overflowCount: overflowing.length,
                    overflowing: overflowing.slice(0, 10)
                };
            })()`,
            returnByValue: true
        });

        console.log("REFINED MOBILE FIX RESULT:");
        console.log(JSON.stringify(evalResult.result.value, null, 2));

        // Take screenshot of Step 1 & Tabs
        const shot1 = await pageClient.send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(ROOT_DIR, 'scratch', 'refined_mobile_step1.png'), Buffer.from(shot1.data, 'base64'));
        console.log("Saved scratch/refined_mobile_step1.png");

        // Scroll down to Form
        await pageClient.send('Runtime.evaluate', { expression: `window.scrollTo(0, 500);` });
        await new Promise(r => setTimeout(r, 400));
        const shot2 = await pageClient.send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(ROOT_DIR, 'scratch', 'refined_mobile_form.png'), Buffer.from(shot2.data, 'base64'));
        console.log("Saved scratch/refined_mobile_form.png");

        // Switch to Preview tab
        await pageClient.send('Runtime.evaluate', { expression: `switchMobileView('preview');` });
        await new Promise(r => setTimeout(r, 400));
        const shot3 = await pageClient.send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(ROOT_DIR, 'scratch', 'refined_mobile_preview.png'), Buffer.from(shot3.data, 'base64'));
        console.log("Saved scratch/refined_mobile_preview.png");

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
