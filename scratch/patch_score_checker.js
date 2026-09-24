const fs = require('fs');

const file = 'resume-score-checker/index.html';
let content = fs.readFileSync(file, 'utf8');

const targetOld = `    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
  <script src="https://unpkg.com/mammoth/mammoth.browser.min.js"></script>
  <script>
    if (window.pdfjsLib) {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
    }`;

const replacementNew = `  <script>
    let _scoreCheckerLibsPromise = null;
    function loadScoreCheckerLibs() {
      if (_scoreCheckerLibsPromise) return _scoreCheckerLibsPromise;
      function loadScript(src) {
        return new Promise((resolve, reject) => {
          const s = document.createElement('script');
          s.src = src;
          s.onload = resolve;
          s.onerror = reject;
          document.head.appendChild(s);
        });
      }
      _scoreCheckerLibsPromise = Promise.all([
        loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js'),
        loadScript('https://unpkg.com/mammoth/mammoth.browser.min.js')
      ]).then(() => {
        if (window.pdfjsLib) {
          window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
        }
      });
      return _scoreCheckerLibsPromise;
    }
    ['touchstart', 'scroll', 'pointerdown', 'focusin', 'dragover'].forEach(evt => {
      window.addEventListener(evt, () => loadScoreCheckerLibs(), { once: true, passive: true });
    });`;

content = content.replace(/\r\n/g, '\n');
const normTarget = targetOld.replace(/\r\n/g, '\n');
const normRep = replacementNew.replace(/\r\n/g, '\n');

if (content.includes(normTarget)) {
  content = content.replace(normTarget, normRep);
  
  // In parseFile(file), add await loadScoreCheckerLibs();
  content = content.replace('async function parseFile(file) {', 'async function parseFile(file) {\n    await loadScoreCheckerLibs();');
  
  fs.writeFileSync(file, content, 'utf8');
  console.log('Successfully patched resume-score-checker/index.html');
} else {
  console.error('Target not matched in resume-score-checker/index.html');
}
