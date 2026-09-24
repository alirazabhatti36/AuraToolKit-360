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
let totalBlocking = 0;
for (const file of htmlFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const headMatch = content.match(/<head[\s\S]*?<\/head>/i);
  if (headMatch) {
    const headContent = headMatch[0];
    const scriptTags = headContent.match(/<script[^>]*>[\s\S]*?<\/script>/gi) || [];
    const blocking = [];
    for (const tag of scriptTags) {
      if (/type=['"]application\/ld\+json['"]/i.test(tag)) continue;
      if (/\b(?:defer|async)\b/i.test(tag)) continue;
      blocking.push(tag);
    }
    if (blocking.length > 0) {
      totalBlocking++;
      console.log(file, 'has', blocking.length, 'blocking scripts in <head>:');
      blocking.forEach(s => {
        const src = s.match(/src=['"]([^'"]+)['"]/i);
        console.log('   ', src ? src[1] : s.substring(0, 60));
      });
    }
  }
}
console.log('Total files with blocking head scripts:', totalBlocking);
