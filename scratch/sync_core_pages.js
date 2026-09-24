const fs = require('fs');

function syncFile(src, dest) {
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
        console.log(`Synced ${src} -> ${dest}`);
    }
}

syncFile('converter/index.html', 'converter.html');
syncFile('converter/index.html', 'templates/converter.html');

syncFile('hr-helper/index.html', 'hr-helper.html');
syncFile('hr-helper/index.html', 'templates/hr-helper.html');

syncFile('resume-score-checker/index.html', 'resume-score-checker.html');
syncFile('resume-score-checker/index.html', 'templates/resume-score-checker.html');

syncFile('resume-cv-maker/index.html', 'resume-cv-maker.html');
syncFile('resume-cv-maker/index.html', 'templates/resume-cv-maker.html');

syncFile('cover-letter-maker/index.html', 'templates/cover-letter-maker.html');
