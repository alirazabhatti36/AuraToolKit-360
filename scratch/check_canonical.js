const fs = require('fs');
const c2 = fs.readFileSync('converter.html', 'utf8');
const match = c2.match(/<link rel="canonical"[^>]+>/);
console.log('converter.html canonical:', match ? match[0] : 'None');
const h2 = fs.readFileSync('hr-helper.html', 'utf8');
const matchH = h2.match(/<link rel="canonical"[^>]+>/);
console.log('hr-helper.html canonical:', matchH ? matchH[0] : 'None');
