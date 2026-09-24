const fs = require('fs');

const page = process.argv[2] || 'resume-cv-maker/index.html';
const content = fs.readFileSync(page, 'utf8');
const scripts = content.match(/<script[^>]*>[\s\S]*?<\/script>/gi) || [];
console.log('Page:', page);
console.log('Total script tags:', scripts.length);
scripts.forEach((s, i) => {
  const src = s.match(/src=['"]([^'"]+)['"]/i);
  if (src) console.log(i, 'SRC:', src[1]);
  else console.log(i, 'INLINE, length:', s.length, 'preview:', s.substring(0, 100).replace(/\n/g, ' '));
});
