const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..');
const PORT = 8094;
const CDP_PORT = 9246;

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.xml': 'application/xml'
};

function startServer() {
    return new Promise(resolve => {
        const server = http.createServer((req, res) => {
            let reqPath = req.url.split('?')[0];
            if (reqPath.endsWith('/')) reqPath += 'index.html';
            let filePath = path.join(ROOT_DIR, reqPath);

            if (!fs.existsSync(filePath) && fs.existsSync(filePath + '.html')) filePath += '.html';

            if (!fs.existsSync(filePath)) {
                res.writeHead(404);
                res.end('Not found: ' + reqPath);
                return;
            }

            if (fs.statSync(filePath).isDirectory()) {
                filePath = path.join(filePath, 'index.html');
            }

            const ext = path.extname(filePath);
            const contentType = MIME_TYPES[ext] || 'application/octet-stream';

            try {
                const content = fs.readFileSync(filePath);
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(content);
            } catch(err) {
                res.writeHead(500);
                res.end('Server Error: ' + err.message);
            }
        });
        server.listen(PORT, '127.0.0.1', () => resolve(server));
    });
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
        } catch(e) {
            await new Promise(r => setTimeout(r, 200));
        }
    }
    throw new Error('CDP port not available');
}

async function main() {
    const server = await startServer();
    console.log(`Test server running at http://localhost:${PORT}`);

    const chromePaths = [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        path.join(process.env.LOCALAPPDATA || '', 'Google\\Chrome\\Application\\chrome.exe')
    ];
    const chromePath = chromePaths.find(p => fs.existsSync(p));
    if (!chromePath) throw new Error('Chrome executable not found');

    const chromeProcess = spawn(chromePath, [
        '--headless=new',
        `--remote-debugging-port=${CDP_PORT}`,
        '--disable-gpu',
        '--no-sandbox',
        'about:blank'
    ]);

    const browserWsUrl = await getDebuggerUrl();
    const browserClient = new CDPClient(browserWsUrl);
    await browserClient.connect();

    const target = await browserClient.send('Target.createTarget', { url: 'about:blank' });
    const pageWsUrl = `ws://127.0.0.1:${CDP_PORT}/devtools/page/${target.targetId}`;
    const pageClient = new CDPClient(pageWsUrl);
    await pageClient.connect();

    await pageClient.send('Page.enable');
    await pageClient.send('DOM.enable');
    await pageClient.send('Runtime.enable');

    const testResults = [];

    async function navigateTo(url) {
        await pageClient.send('Page.navigate', { url });
        await new Promise(r => setTimeout(r, 1000));
        await pageClient.send('Runtime.evaluate', {
            expression: 'window.alert = function(){}; window.confirm = function(){ return true; };'
        });
    }

    // --- TEST 1: /resume-score-checker/widget/ ---
    console.log('\n--- Test 1: Testing /resume-score-checker/widget/ ---');
    await navigateTo(`http://localhost:${PORT}/resume-score-checker/widget/`);

    let evalWidget = await pageClient.send('Runtime.evaluate', {
        expression: `(() => {
            const container = document.querySelector('.widget-container');
            const dropzone = document.getElementById('dropzone');
            const scanBtn = document.getElementById('scanBtn');
            const attribution = document.querySelector('.widget-attribution a');
            return {
                containerExists: !!container,
                dropzoneExists: !!dropzone,
                scanBtnExists: !!scanBtn,
                attributionHref: attribution ? attribution.href : null,
                attributionText: attribution ? attribution.textContent : null
            };
        })()`,
        returnByValue: true
    });
    console.log('Widget initial check:', JSON.stringify(evalWidget.result.value, null, 2));

    let evalWidgetScan = await pageClient.send('Runtime.evaluate', {
        expression: `(() => {
            const fakeFile = new File([
                "Jane Doe\\nSoftware Engineer\\njane@example.com | 123-456-7890 | linkedin.com/in/janedoe\\n\\n" +
                "Summary: Results-driven engineer with 5 years experience in web applications.\\n\\n" +
                "Work Experience:\\nSenior Developer at Tech Corp\\n- Managed and built high performance systems.\\n" +
                "- Spearheaded cloud migration and automated CI/CD pipelines, increasing performance by 40%.\\n\\n" +
                "Education:\\nBS in Computer Science\\n\\nSkills:\\nJavaScript, Python, React, Node.js, SQL, Docker, Git"
            ], "jane_resume.txt", { type: "text/plain" });

            handleFileSelect([fakeFile]);
            triggerScan();

            return new Promise((resolve) => {
                setTimeout(() => {
                    const resultsView = document.getElementById('resultsView');
                    const score = document.getElementById('scoreValue').textContent;
                    const grade = document.getElementById('gradeBadge').textContent;
                    const matchedTags = document.getElementById('widgetMatchedTags').children.length;
                    const fullAuditBtn = document.querySelector('.btn-full-audit');
                    resolve({
                        resultsVisible: resultsView && resultsView.style.display === 'block',
                        score,
                        grade,
                        matchedTagsCount: matchedTags,
                        fullAuditHref: fullAuditBtn ? fullAuditBtn.href : null
                    });
                }, 500);
            });
        })()`,
        awaitPromise: true,
        returnByValue: true
    });
    console.log('Widget scan check:', JSON.stringify(evalWidgetScan.result.value, null, 2));

    const widgetPassed = evalWidget.result.value.containerExists &&
                         evalWidget.result.value.attributionHref && evalWidget.result.value.attributionHref.includes('auratoolkit360.com') &&
                         evalWidgetScan.result.value.resultsVisible &&
                         evalWidgetScan.result.value.score.includes('%');
    testResults.push({ name: 'ATS Scorecard Widget (/resume-score-checker/widget/)', passed: widgetPassed });

    // --- TEST 2: /resume-score-checker/ Embed Snippet Box ---
    console.log('\n--- Test 2: Testing /resume-score-checker/ Embed Generator ---');
    await navigateTo(`http://localhost:${PORT}/resume-score-checker/`);

    let evalEmbedBox = await pageClient.send('Runtime.evaluate', {
        expression: `(() => {
            const embedTextarea = document.getElementById('widgetEmbedCode');
            const copyBtn = document.getElementById('copyEmbedBtn');
            const embedVal = embedTextarea ? embedTextarea.value : '';
            return {
                embedTextareaExists: !!embedTextarea,
                copyBtnExists: !!copyBtn,
                containsIframe: embedVal.includes('<iframe') && embedVal.includes('/resume-score-checker/widget/'),
                containsAttribution: embedVal.includes('AuraToolKit 360')
            };
        })()`,
        returnByValue: true
    });
    console.log('Embed box check:', JSON.stringify(evalEmbedBox.result.value, null, 2));

    const embedPassed = evalEmbedBox.result.value.embedTextareaExists &&
                        evalEmbedBox.result.value.containsIframe &&
                        evalEmbedBox.result.value.containsAttribution;
    testResults.push({ name: 'Embed Generator Box on ATS Score Checker', passed: embedPassed });

    // --- TEST 3: Modernized Converter Pages (Word to PDF, OCR, Passport Photo) ---
    const converterPages = [
        { path: '/converter/word-to-pdf/', name: 'Word to PDF Converter' },
        { path: '/converter/ocr-to-text/', name: 'OCR to Text Scanner' },
        { path: '/converter/passport-photo-maker/', name: 'Passport Photo Maker' }
    ];

    for (const page of converterPages) {
        console.log(`\n--- Test: Testing ${page.name} (${page.path}) ---`);
        await navigateTo(`http://localhost:${PORT}${page.path}`);

        // Viewport 1440px
        await pageClient.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
        await new Promise(r => setTimeout(r, 200));

        let evalPage = await pageClient.send('Runtime.evaluate', {
            expression: `(() => {
                const navbar = document.querySelector('.navbar');
                const navHeight = navbar ? navbar.getBoundingClientRect().height : 0;
                const h1 = document.querySelector('h1');
                const toolCard = document.querySelector('.tool-card');
                const schemas = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
                let parsedSchemas = [];
                let hasSoftwareApp = false, hasHowTo = false, hasFAQ = false;

                schemas.forEach(s => {
                    try {
                        const json = JSON.parse(s.textContent);
                        const graph = json['@graph'] || [json];
                        graph.forEach(item => {
                            if (item['@type'] === 'SoftwareApplication') hasSoftwareApp = true;
                            if (item['@type'] === 'HowTo') hasHowTo = true;
                            if (item['@type'] === 'FAQPage') hasFAQ = true;
                        });
                        parsedSchemas.push(json);
                    } catch(e) {}
                });

                const bodyWidth = document.body.scrollWidth;
                const windowWidth = window.innerWidth;

                return {
                    navHeight: Math.round(navHeight),
                    hasH1: !!h1,
                    hasToolCard: !!toolCard,
                    hasSoftwareApp,
                    hasHowTo,
                    hasFAQ,
                    overflow: bodyWidth > windowWidth
                };
            })()`,
            returnByValue: true
        });
        console.log(`${page.name} 1440px check:`, JSON.stringify(evalPage.result.value, null, 2));

        // Mobile Viewport 375px
        await pageClient.send('Emulation.setDeviceMetricsOverride', { width: 375, height: 667, deviceScaleFactor: 1, mobile: true });
        await new Promise(r => setTimeout(r, 200));

        let evalMobile = await pageClient.send('Runtime.evaluate', {
            expression: `(() => {
                const bodyWidth = document.body.scrollWidth;
                const windowWidth = window.innerWidth;
                const hamburger = document.getElementById('navHamburger');
                return {
                    overflowMobile: bodyWidth > windowWidth,
                    hamburgerVisible: hamburger ? window.getComputedStyle(hamburger).display !== 'none' : false
                };
            })()`,
            returnByValue: true
        });
        console.log(`${page.name} 375px mobile check:`, JSON.stringify(evalMobile.result.value, null, 2));

        const pagePassed = evalPage.result.value.navHeight === 66 &&
                           evalPage.result.value.hasSoftwareApp &&
                           evalPage.result.value.hasHowTo &&
                           evalPage.result.value.hasFAQ &&
                           !evalPage.result.value.overflow &&
                           !evalMobile.result.value.overflowMobile;

        testResults.push({ name: `${page.name} (Navbar, Schema, Responsive)`, passed: pagePassed });
    }

    // --- TEST 4: sitemap.xml Validation ---
    console.log('\n--- Test 4: Testing sitemap.xml ---');
    const sitemapContent = fs.readFileSync(path.join(ROOT_DIR, 'sitemap.xml'), 'utf8');
    const sitemapPassed = sitemapContent.includes('<loc>https://auratoolkit360.com/resume-score-checker/widget/</loc>') &&
                          sitemapContent.includes('<loc>https://auratoolkit360.com/converter/word-to-pdf/</loc>') &&
                          sitemapContent.includes('<loc>https://auratoolkit360.com/converter/ocr-to-text/</loc>') &&
                          sitemapContent.includes('<loc>https://auratoolkit360.com/converter/passport-photo-maker/</loc>') &&
                          sitemapContent.includes('<priority>0.9</priority>');
    testResults.push({ name: 'Sitemap XML Registration & Priorities', passed: sitemapPassed });

    // Cleanup
    browserClient.close();
    pageClient.close();
    chromeProcess.kill();
    server.close();

    console.log('\n=========================================');
    console.log('       PHASE 3 VERIFICATION SUMMARY       ');
    console.log('=========================================');
    let allPassed = true;
    for (const r of testResults) {
        console.log(`${r.passed ? '✅ PASS' : '❌ FAIL'}: ${r.name}`);
        if (!r.passed) allPassed = false;
    }
    console.log('=========================================');

    if (!allPassed) process.exit(1);
}

main().catch(err => {
    console.error('Test execution error:', err);
    process.exit(1);
});
