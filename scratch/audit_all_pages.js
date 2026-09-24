const fs = require('fs');
const path = require('path');

function getAllHtml(dir, list = []) {
    fs.readdirSync(dir).forEach(f => {
        if (f === 'node_modules' || f === '.git' || f === 'scratch') return;
        const full = path.join(dir, f);
        if (fs.statSync(full).isDirectory()) getAllHtml(full, list);
        else if (f.endsWith('.html')) list.push(full);
    });
    return list;
}

const all = getAllHtml('.');
let syncFonts = [], asyncFonts = 0;
let syncSocial = [], asyncSocial = 0;
let syncLang = [], asyncLang = 0;
let hasDirectAdsense = [];
let hasHeavyBlurOnMobile = [];

all.forEach(file => {
    const c = fs.readFileSync(file, 'utf8');
    if (c.includes('fonts.googleapis.com')) {
        if (c.includes('rel="preload" as="style" href="https://fonts.googleapis.com')) {
            asyncFonts++;
        } else {
            syncFonts.push(file);
        }
    }
    if (c.includes('social-share.css')) {
        if (c.includes('media="print"')) {
            asyncSocial++;
        } else {
            syncSocial.push(file);
        }
    }
    if (c.includes('lang-switcher.css')) {
        if (c.includes('media="print"')) {
            asyncLang++;
        } else {
            syncLang.push(file);
        }
    }
    if (c.includes('pagead2.googlesyndication.com/pagead/js/adsbygoogle.js')) {
        hasDirectAdsense.push(file);
    }
    if (c.includes('.ambient-glow') && !c.includes('@media (max-width: 768px)') && !c.includes('@media (max-width: 960px)')) {
        hasHeavyBlurOnMobile.push(file);
    }
});

console.log('Total HTML files analyzed:', all.length);
console.log('Fonts -> Sync (BLOCKING):', syncFonts.length, 'Async (Fast):', asyncFonts);
console.log('Social CSS -> Sync (BLOCKING):', syncSocial.length, 'Async (Fast):', asyncSocial);
console.log('Lang CSS -> Sync (BLOCKING):', syncLang.length, 'Async (Fast):', asyncLang);
console.log('Files with direct blocking adsbygoogle.js:', hasDirectAdsense.length);
console.log('\nSample Sync Fonts Files:', syncFonts.slice(0, 10));
console.log('\nSample Sync Social Files:', syncSocial.slice(0, 10));
console.log('\nSample Sync Lang Files:', syncLang.slice(0, 10));
