const fs = require('fs');

function patchCoverLetter(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Fix noscript extra >
    content = content.replace('</noscript>>', '</noscript>');
    
    // Remove blocking head scripts
    const headScripts = `    <!-- Client-Side PDF & DOCX Generation -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>`;
    
    content = content.replace(/\r\n/g, '\n');
    const normHeadScripts = headScripts.replace(/\r\n/g, '\n');
    
    if (content.includes(normHeadScripts)) {
        content = content.replace(normHeadScripts, '');
    } else {
        // Fallback replacement for script tags
        content = content.replace(/<script src="https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/html2pdf\.js\/0\.10\.1\/html2pdf\.bundle\.min\.js"><\/script>\s*/g, '');
        content = content.replace(/<script src="https:\/\/cdn\.jsdelivr\.net\/npm\/docx@8\.5\.0\/build\/index\.min\.js"><\/script>\s*/g, '');
        content = content.replace(/<script src="https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/FileSaver\.js\/2\.0\.5\/FileSaver\.min\.js"><\/script>\s*/g, '');
        content = content.replace(/<!-- Client-Side PDF & DOCX Generation -->\s*/g, '');
    }
    
    // Add library loader before downloadLetterPDF
    const loaderCode = `
        let clLibsPromise = null;
        function loadCoverLetterLibraries() {
            if (clLibsPromise) return clLibsPromise;
            function loadScript(src) {
                return new Promise((resolve, reject) => {
                    const s = document.createElement('script');
                    s.src = src;
                    s.onload = resolve;
                    s.onerror = reject;
                    document.head.appendChild(s);
                });
            }
            clLibsPromise = Promise.all([
                loadScript('https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js'),
                loadScript('https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.min.js'),
                loadScript('https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js')
            ]);
            return clLibsPromise;
        }
        ['touchstart', 'scroll', 'pointerdown', 'focusin'].forEach(evt => {
            window.addEventListener(evt, () => loadCoverLetterLibraries(), { once: true, passive: true });
        });

        async function downloadLetterPDF() {
            await loadCoverLetterLibraries();`;
            
    content = content.replace('function downloadLetterPDF() {', loaderCode);
    
    // In downloadLetterDOCX, add await loadCoverLetterLibraries();
    content = content.replace('async function downloadLetterDOCX() {', 'async function downloadLetterDOCX() {\n            await loadCoverLetterLibraries();');
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Patched:', filePath);
}

patchCoverLetter('cover-letter-maker/index.html');
if (fs.existsSync('templates/cover-letter-maker.html')) {
    patchCoverLetter('templates/cover-letter-maker.html');
}
