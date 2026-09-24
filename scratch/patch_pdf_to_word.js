const fs = require('fs');

const file = 'converter/pdf-to-word/index.html';
const staticBlockRegex = /<!-- Comprehensive Client-Side Conversion Libraries -->[\s\S]*?<script src="https:\/\/cdn\.jsdelivr\.net\/npm\/docx@7\.8\.2\/build\/index\.js"><\/script>/i;

const dynamicLoader = `<!-- Comprehensive Client-Side Conversion Libraries (Loaded on User Interaction) -->
    <script>
        let _converterScriptsLoaded = false;
        function loadConverterLibraries() {
            if (_converterScriptsLoaded) return;
            _converterScriptsLoaded = true;
            const libs = [
                'https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js',
                'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js',
                'https://cdn.jsdelivr.net/npm/mammoth@1.6.0/mammoth.browser.min.js',
                'https://cdn.jsdelivr.net/npm/docx@7.8.2/build/index.js'
            ];
            libs.forEach(src => {
                if (!document.querySelector(\`script[src="\${src}"]\`)) {
                    const s = document.createElement('script');
                    s.src = src;
                    s.async = true;
                    if (src.includes('pdf.min.js')) {
                        s.onload = () => {
                            if (window.pdfjsLib) {
                                window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
                            }
                        };
                    }
                    document.head.appendChild(s);
                }
            });
        }

        // Prefetch on first touch, scroll, or file input focus
        ['touchstart', 'scroll', 'pointerdown', 'focusin'].forEach(evt => {
            window.addEventListener(evt, loadConverterLibraries, { once: true, passive: true });
        });
    </script>`;

let content = fs.readFileSync(file, 'utf8');
if (staticBlockRegex.test(content)) {
  content = content.replace(staticBlockRegex, dynamicLoader);
  fs.writeFileSync(file, content, 'utf8');
  console.log('Patched:', file);
} else {
  console.log('Not matched');
}
