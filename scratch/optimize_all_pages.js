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

const fontReplacement = `<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="font" type="font/woff2" href="https://fonts.gstatic.com/s/plusjakartasans/v12/LDIoaomQNQcsA88c7O9yZ4KMCoOg4Ko20yygg_vb.woff2" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=optional" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=optional"></noscript>`;

const socialReplacement = `<link rel="stylesheet" href="/assets/social-share.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="/assets/social-share.css"></noscript>`;

const langReplacement = `<link rel="stylesheet" href="/assets/lang-switcher.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="/assets/lang-switcher.css"></noscript>`;

const ambientMobileCss = `
        @media (max-width: 768px) {
            .ambient-glow-top-left, .ambient-glow-top-right, .ambient-glow-mid {
                display: none !important;
            }
        }
`;

const files = getAllHtml('.');
let updatedCount = 0;

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let original = content;

    // 1. Remove direct adsbygoogle.js script tag
    content = content.replace(/<script async src="https:\/\/pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js[^"]*"[^>]*><\/script>\s*/g, '');

    // 2. Optimize Google Fonts
    // Match old preconnect + link font pattern
    const oldFontRegex = /<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com">\s*(<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com"[^>]*>\s*)?(<link rel="preload" as="font"[^>]*>\s*)?<link (href="https:\/\/fonts\.googleapis\.com\/css2\?[^"]*" rel="stylesheet"|rel="preload" as="style" href="https:\/\/fonts\.googleapis\.com\/css2\?[^"]*"[^>]*>)\s*(<noscript><link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com\/css2\?[^"]*"><\/noscript>)?/;
    
    if (oldFontRegex.test(content)) {
        content = content.replace(oldFontRegex, fontReplacement);
    } else if (content.includes('fonts.googleapis.com/css2?family=')) {
        // Fallback replacement for font link
        content = content.replace(/<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com">\s*(<link rel="preconnect" href="https:\/\/fonts\.gstatic\.com"[^>]*>\s*)?<link[^>]*href="https:\/\/fonts\.googleapis\.com\/css2\?[^"]*"[^>]*>\s*(<noscript><link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com\/css2\?[^"]*"><\/noscript>)?/, fontReplacement);
    }

    // 3. Optimize social-share.css (only if synchronous)
    content = content.replace(/<link rel="stylesheet" href="\/assets\/social-share\.css">(?!\s*<noscript>)/g, socialReplacement);

    // 4. Optimize lang-switcher.css (only if synchronous)
    content = content.replace(/<link rel="stylesheet" href="\/assets\/lang-switcher\.css">(?!\s*<noscript>)/g, langReplacement);

    // 5. Ambient glow mobile optimization
    if (content.includes('.ambient-glow-top-left') && !content.includes('.ambient-glow-top-left, .ambient-glow-top-right') && !content.includes('.ambient-glow-top-left,\n            .ambient-glow-top-right') && !content.includes('.ambient-glow-top-left,\r\n            .ambient-glow-top-right')) {
        content = content.replace('</style>', ambientMobileCss + '    </style>');
    }

    if (content !== original) {
        fs.writeFileSync(file, content, 'utf8');
        updatedCount++;
    }
});

console.log(`Successfully optimized ${updatedCount} HTML files across the website.`);
