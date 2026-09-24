const fs = require('fs');

function findFiles(dir, list = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', '.git', 'scratch'].includes(e.name)) continue;
    const full = dir + '/' + e.name;
    if (e.isDirectory()) findFiles(full, list);
    else if (e.name.endsWith('.html')) list.push(full);
  }
  return list;
}

const htmlFiles = findFiles('.');
const heavyLibs = [
  'pdf.min.js',
  'mammoth.browser.min.js',
  'tesseract.min.js',
  'pdf-lib.min.js'
];

for (const lib of heavyLibs) {
  const staticFound = [];
  for (const f of htmlFiles) {
    const content = fs.readFileSync(f, 'utf8');
    const regex = new RegExp('<script[^>]+src=["\'][^"\']*' + lib.replace('.', '\\.') + '["\']', 'i');
    if (regex.test(content)) {
      staticFound.push(f);
    }
  }
  console.log(`Static tag for ${lib}: found in ${staticFound.length} files:`);
  console.log(staticFound);
}
