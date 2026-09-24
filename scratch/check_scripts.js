const fs = require('fs');
const path = require('path');

function getHtmlFiles(dir) {
  let files = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (['node_modules', '.git', 'scratch', '.gemini'].includes(entry.name)) continue;
      files = files.concat(getHtmlFiles(full));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      files.push(full);
    }
  }
  return files;
}

const htmlFiles = getHtmlFiles('.');
const fileToScripts = {};

for (const file of htmlFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const matches = content.match(/<script[^>]+src=[^>]+>/gi);
  if (matches) {
    for (const tag of matches) {
      const srcMatch = tag.match(/src=["']([^"']+)["']/i);
      if (srcMatch) {
        const src = srcMatch[1];
        if (src.startsWith('http') || src.includes('cdn')) {
          if (!fileToScripts[file]) fileToScripts[file] = [];
          fileToScripts[file].push(src);
        }
      }
    }
  }
}

for (const [file, scripts] of Object.entries(fileToScripts)) {
  console.log(file, 'has', scripts.length, 'external scripts:');
  for (const s of scripts) {
    console.log('   ', s);
  }
}
