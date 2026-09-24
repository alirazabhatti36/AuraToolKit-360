const fs = require('fs');

const master = fs.readFileSync('resume-cv-maker/index.html', 'utf8');

fs.writeFileSync('resume-cv-maker.html', master, 'utf8');
console.log('Synced resume-cv-maker.html');

fs.writeFileSync('templates/resume-cv-maker.html', master, 'utf8');
console.log('Synced templates/resume-cv-maker.html');
