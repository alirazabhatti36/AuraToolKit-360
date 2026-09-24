const { execSync } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = 'c:\\Users\\Ali Raza Bhatti\\Desktop\\AuraToolKit 360';
const PORT = 8096;

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

server.listen(PORT, '127.0.0.1', () => {
    console.log(`Server running at http://127.0.0.1:${PORT}/`);
    try {
        const cmd = `npx lighthouse "http://127.0.0.1:${PORT}/resume-cv-maker/" --output=json --output-path=scratch/lh_local_test.json --form-factor=mobile --screenEmulation.mobile --only-categories=performance --chrome-flags="--headless=new --no-sandbox"`;
        execSync(cmd, { stdio: 'inherit', cwd: ROOT_DIR });
        
        const report = JSON.parse(fs.readFileSync(path.join(ROOT_DIR, 'scratch', 'lh_local_test.json'), 'utf8'));
        const score = Math.round(report.categories.performance.score * 100);
        console.log(`\n================================`);
        console.log(`LOCAL MOBILE PERFORMANCE SCORE: ${score}`);
        console.log(`================================\n`);
        const a = report.audits;
        console.log('FCP:', a['first-contentful-paint'].displayValue);
        console.log('LCP:', a['largest-contentful-paint'].displayValue);
        console.log('TBT:', a['total-blocking-time'].displayValue);
        console.log('CLS:', a['cumulative-layout-shift'].displayValue);
        console.log('Speed Index:', a['speed-index'].displayValue);
    } catch (err) {
        console.error('Lighthouse execution error:', err.message);
        if (fs.existsSync(path.join(ROOT_DIR, 'scratch', 'lh_local_test.json'))) {
            const report = JSON.parse(fs.readFileSync(path.join(ROOT_DIR, 'scratch', 'lh_local_test.json'), 'utf8'));
            const score = Math.round(report.categories.performance.score * 100);
            console.log(`\n================================`);
            console.log(`LOCAL MOBILE PERFORMANCE SCORE: ${score}`);
            console.log(`================================\n`);
            const a = report.audits;
            console.log('FCP:', a['first-contentful-paint'].displayValue);
            console.log('LCP:', a['largest-contentful-paint'].displayValue);
            console.log('TBT:', a['total-blocking-time'].displayValue);
            console.log('CLS:', a['cumulative-layout-shift'].displayValue);
            console.log('Speed Index:', a['speed-index'].displayValue);
        }
    } finally {
        server.close();
        process.exit(0);
    }
});
