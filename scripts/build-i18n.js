const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');

const LANGS = JSON.parse(fs.readFileSync(path.join(__dirname, 'languages.json'), 'utf8'));

const EN_KEYWORD_FIRST_SEO = {
    home: {
        title: 'Free Online File Converter & ATS Resume Builder | AuraToolkit360',
        desc: 'Convert PDF to Word, Word to PDF, build ATS-friendly resumes, scan CV match scores, and screen candidates privately in your browser. 100% free, no sign-up.',
        keywords: 'convert pdf to word free, free online file converter, ats resume builder free, resume score checker, bulk resume screener, merge pdf online, AuraToolkit360'
    },
    converter: {
        title: 'Free Online File Converter Suite (30+ PDF & Office Tools) | AuraToolkit360',
        desc: 'Convert, merge, compress, and edit PDF, Word, Excel, JPG, and video files locally in your browser. Fast, secure, and 100% private.',
        keywords: 'free file converter online, pdf to word converter without email, merge pdf files free, compress pdf, docx to pdf, private file tools'
    },
    resume: {
        title: 'Free ATS Resume Builder & Professional CV Maker | AuraToolkit360',
        desc: 'Build recruiter-approved, 100% ATS-compliant resumes with 7 modern templates. Instant PDF & Word DOCX download without account creation.',
        keywords: 'free ats resume builder, ats friendly resume maker no sign up, professional cv creator free, download resume docx pdf, private resume builder'
    },
    score_checker: {
        title: 'Free ATS Resume Score Checker & Keyword Scanner | AuraToolkit360',
        desc: 'Scan your resume against job descriptions for instant ATS match scoring, missing keyword analysis, and recruiter insights 100% privately in browser.',
        keywords: 'free ats resume checker, check resume score online, resume keyword scanner, ats compatibility tester, optimize resume for job description'
    },
    hr_helper: {
        title: 'Free HR Bulk Resume Screener & Candidate Filter | AuraToolkit360',
        desc: 'Screen and rank up to 300+ candidate CVs locally in your browser with automated keyword matching, ATS scoring, and instant CSV/ZIP export.',
        keywords: 'bulk resume screening tool, free candidate filter for recruiters, hr resume scanner, shortlist candidates offline, hr helper'
    }
};

function generateHreflangTags(pagePath) {
    const base = 'https://auratoolkit360.com';
    const trailing = pagePath ? (pagePath.endsWith('/') ? pagePath : pagePath + '/') : '';
    let tags = '    <link rel="alternate" hreflang="x-default" href="' + base + '/' + trailing + '">\n';
    tags += '    <link rel="alternate" hreflang="en" href="' + base + '/' + trailing + '">\n';
    LANGS.forEach(l => {
        tags += '    <link rel="alternate" hreflang="' + l.code + '" href="' + base + '/' + l.code + '/' + trailing + '">\n';
    });
    return tags;
}

function generateLangSwitcherHtml(currentLangCode, pagePath) {
    const currentObj = LANGS.find(l => l.code === currentLangCode) || { code: 'en', flag: '🇺🇸', name: 'English' };
    const trailing = pagePath ? (pagePath.endsWith('/') ? pagePath : pagePath + '/') : '';

    return '<div class="lang-switcher" id="langSwitcherContainer">\n' +
           '    <button class="lang-switcher-btn" id="langSwitcherBtn" onclick="toggleLangDropdown(event)" aria-label="Select Language" aria-expanded="false" aria-haspopup="true">\n' +
           '        <span class="lang-globe">🌐</span>\n' +
           '        <span class="lang-current-flag">' + currentObj.flag + '</span>\n' +
           '        <span class="lang-current-label">' + currentObj.code.toUpperCase() + '</span>\n' +
           '        <span class="lang-arrow">▾</span>\n' +
           '    </button>\n' +
           '    <div class="lang-dropdown-menu" id="langDropdownMenu" role="menu">\n' +
           '        <a href="/' + trailing + '" class="lang-option ' + (currentLangCode === 'en' ? 'active' : '') + '" data-lang="en" role="menuitem"><span class="flag">🇺🇸</span> English</a>\n' +
           LANGS.map(l => '        <a href="/' + l.code + '/' + trailing + '" class="lang-option ' + (currentLangCode === l.code ? 'active' : '') + '" data-lang="' + l.code + '" role="menuitem"><span class="flag">' + l.flag + '</span> ' + l.name + '</a>').join('\n') + '\n' +
           '    </div>\n' +
           '</div>';
}

function generateMobileLangSwitcherHtml(currentLangCode, pagePath) {
    const trailing = pagePath ? (pagePath.endsWith('/') ? pagePath : pagePath + '/') : '';
    return '<div class="mobile-lang-container">\n' +
           '    <div class="mobile-lang-title">🌐 Language / Idioma / Sprache</div>\n' +
           '    <div class="mobile-lang-grid">\n' +
           '        <a href="/' + trailing + '" class="mobile-lang-item ' + (currentLangCode === 'en' ? 'active' : '') + '" data-lang="en"><span class="flag">🇺🇸</span> EN</a>\n' +
           LANGS.map(l => '        <a href="/' + l.code + '/' + trailing + '" class="mobile-lang-item ' + (currentLangCode === l.code ? 'active' : '') + '" data-lang="' + l.code + '"><span class="flag">' + l.flag + '</span> ' + l.code.toUpperCase() + '</a>').join('\n') + '\n' +
           '    </div>\n' +
           '</div>';
}

function updateEnglishFile(filePath, pageKey, pagePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    const seo = EN_KEYWORD_FIRST_SEO[pageKey];

    content = content.replace(/<title>[^<]+<\/title>/, '<title>' + seo.title + '</title>');
    content = content.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="' + seo.desc + '">');
    content = content.replace(/<meta name="keywords" content="[^"]*">/, '<meta name="keywords" content="' + seo.keywords + '">');
    content = content.replace(/<meta property="og:title" content="[^"]*">/, '<meta property="og:title" content="' + seo.title + '">');
    content = content.replace(/<meta property="og:description" content="[^"]*">/, '<meta property="og:description" content="' + seo.desc + '">');
    content = content.replace(/<meta name="twitter:title" content="[^"]*">/, '<meta name="twitter:title" content="' + seo.title + '">');
    content = content.replace(/<meta name="twitter:description" content="[^"]*">/, '<meta name="twitter:description" content="' + seo.desc + '">');

    if (!content.includes('hreflang="x-default"')) {
        const hreflangTags = generateHreflangTags(pagePath);
        content = content.replace(/<link rel="canonical"[^>]*>/, '$&\n' + hreflangTags);
    }

    if (!content.includes('lang-switcher.css')) {
        content = content.replace('</head>', '    <link rel="stylesheet" href="/assets/lang-switcher.css">\n    <script defer src="/assets/lang-switcher.js"></script>\n</head>');
    }

    if (!content.includes('id="langSwitcherBtn"')) {
        const switcherHtml = generateLangSwitcherHtml('en', pagePath);
        content = content.replace(/(<button class="nav-hamburger"[^>]*>)/, switcherHtml + '\n                $1');
    }

    if (!content.includes('class="mobile-lang-container"')) {
        const mobileSwitcherHtml = generateMobileLangSwitcherHtml('en', pagePath);
        content = content.replace(/(<\/div>\s*<\/div>\s*<\/nav>)/, mobileSwitcherHtml + '\n            $1');
    }

    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Updated English file: ' + filePath);
}

function generateLocalizedFile(sourceFilePath, targetFilePath, lang, pageKey, pagePath) {
    let content = fs.readFileSync(sourceFilePath, 'utf8');
    const seo = lang.seo[pageKey];
    const targetDir = path.dirname(targetFilePath);
    if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
    }

    content = content.replace(/<html\s+lang="[^"]*"/, '<html lang="' + lang.code + '"' + (lang.dir === 'rtl' ? ' dir="rtl"' : ''));

    const canonicalUrl = 'https://auratoolkit360.com/' + lang.code + '/' + (pagePath ? (pagePath.endsWith('/') ? pagePath : pagePath + '/') : '');
    content = content.replace(/<link rel="canonical"\s+href="[^"]*">/, '<link rel="canonical" href="' + canonicalUrl + '">');

    content = content.replace(/<title>[^<]+<\/title>/, '<title>' + seo.title + '</title>');
    content = content.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="' + seo.desc + '">');
    content = content.replace(/<meta name="keywords" content="[^"]*">/, '<meta name="keywords" content="' + seo.keywords + '">');
    content = content.replace(/<meta property="og:title" content="[^"]*">/, '<meta property="og:title" content="' + seo.title + '">');
    content = content.replace(/<meta property="og:description" content="[^"]*">/, '<meta property="og:description" content="' + seo.desc + '">');
    content = content.replace(/<meta property="og:url" content="[^"]*">/, '<meta property="og:url" content="' + canonicalUrl + '">');
    content = content.replace(/<meta name="twitter:title" content="[^"]*">/, '<meta name="twitter:title" content="' + seo.title + '">');
    content = content.replace(/<meta name="twitter:description" content="[^"]*">/, '<meta name="twitter:description" content="' + seo.desc + '">');
    content = content.replace(/"inLanguage":\s*"en"/g, '"inLanguage": "' + lang.code + '"');

    if (!content.includes('hreflang="x-default"')) {
        const hreflangTags = generateHreflangTags(pagePath);
        content = content.replace(/<link rel="canonical"[^>]*>/, '$&\n' + hreflangTags);
    }

    if (!content.includes('lang-switcher.css')) {
        content = content.replace('</head>', '    <link rel="stylesheet" href="/assets/lang-switcher.css">\n    <script defer src="/assets/lang-switcher.js"></script>\n</head>');
    }

    const switcherHtml = generateLangSwitcherHtml(lang.code, pagePath);
    if (!content.includes('id="langSwitcherBtn"')) {
        content = content.replace(/(<button class="nav-hamburger"[^>]*>)/, switcherHtml + '\n                $1');
    } else {
        content = content.replace(/<div class="lang-switcher" id="langSwitcherContainer">[\s\S]*?<\/div>\s*<\/div>/, switcherHtml);
    }

    if (!content.includes('class="mobile-lang-container"')) {
        const mobileSwitcherHtml = generateMobileLangSwitcherHtml(lang.code, pagePath);
        content = content.replace(/(<\/div>\s*<\/div>\s*<\/nav>)/, mobileSwitcherHtml + '\n            $1');
    }

    // Localize navigation
    content = content.replace(/<a href="\/" class="nav-link([^"]*)">Home<\/a>/, '<a href="/' + lang.code + '/\" class="nav-link$1">' + lang.nav.home + '</a>');
    content = content.replace(/<a href="\/converter\/" class="nav-link([^"]*)">Converter<\/a>/, '<a href="/' + lang.code + '/converter/\" class="nav-link$1">' + lang.nav.converter + '</a>');
    content = content.replace(/<a href="\/resume-cv-maker\/" class="nav-link([^"]*)">Resume<\/a>/, '<a href="/' + lang.code + '/resume-cv-maker/\" class="nav-link$1">' + lang.nav.resume + '</a>');
    content = content.replace(/<a href="\/cover-letter-maker\/" class="nav-link([^"]*)">Cover Letter<\/a>/, '<a href="/cover-letter-maker/\" class="nav-link$1">' + lang.nav.cover_letter + '</a>');
    content = content.replace(/<a href="\/resume-score-checker\/" class="nav-link([^"]*)">Score Checker<\/a>/, '<a href="/' + lang.code + '/resume-score-checker/\" class="nav-link$1">' + lang.nav.score_checker + '</a>');
    content = content.replace(/<a href="\/hr-helper\/" class="nav-link([^"]*)">HR Bulk/, '<a href="/' + lang.code + '/hr-helper/\" class="nav-link$1">' + lang.nav.hr_helper);
    content = content.replace(/<a href="\/blogs\/" class="nav-link">Blogs<\/a>/, '<a href="/blogs/\" class="nav-link">' + lang.nav.blogs + '</a>');
    content = content.replace(/<a href="\/about\/" class="nav-link">About<\/a>/, '<a href="/about/\" class="nav-link">' + lang.nav.about + '</a>');
    content = content.replace(/<a href="\/hr-helper\/" class="btn-try-hr">Try HR Helper →<\/a>/, '<a href="/' + lang.code + '/hr-helper/\" class="btn-try-hr">' + lang.nav.try_hr + '</a>');
    content = content.replace(/<button class="btn-bookmark-nav"[^>]*>★ Bookmark<\/button>/, '<button class="btn-bookmark-nav" onclick="bookmarkSite()">' + lang.nav.bookmark + '</button>');
    content = content.replace(/<a href="\/" class="logo">/, '<a href="/' + lang.code + '/\" class="logo">');

    // RTL for Arabic
    if (lang.dir === 'rtl') {
        const rtlCss = '<style>\n' +
                       '    [dir="rtl"] { direction: rtl; text-align: right; }\n' +
                       '    [dir="rtl"] .nav-center { flex-direction: row-reverse; }\n' +
                       '    [dir="rtl"] .nav-right-actions { flex-direction: row-reverse; }\n' +
                       '    [dir="rtl"] .tool-features, [dir="rtl"] .stats-summary-grid { direction: rtl; }\n' +
                       '    [dir="rtl"] .lang-dropdown-menu { right: auto !important; left: 0 !important; text-align: right; }\n' +
                       '</style>';
        content = content.replace('</head>', rtlCss + '\n</head>');
    }

    fs.writeFileSync(targetFilePath, content, 'utf8');
    console.log('Generated: ' + targetFilePath);
}

const PAGES = [
    { key: 'home', path: '', source: 'index.html' },
    { key: 'converter', path: 'converter/', source: 'converter/index.html' },
    { key: 'resume', path: 'resume-cv-maker/', source: 'resume-cv-maker/index.html' },
    { key: 'score_checker', path: 'resume-score-checker/', source: 'resume-score-checker/index.html' },
    { key: 'hr_helper', path: 'hr-helper/', source: 'hr-helper/index.html' }
];

console.log('=== Step 1: Updating English Master Pages ===');
PAGES.forEach(p => {
    const src = path.join(ROOT_DIR, p.source);
    if (fs.existsSync(src)) {
        updateEnglishFile(src, p.key, p.path);
    }
});

console.log('=== Step 2: Generating Localized Pages for 5 Languages ===');
LANGS.forEach(lang => {
    console.log('\n--- Compiling: ' + lang.name + ' (' + lang.code.toUpperCase() + ') ---');
    PAGES.forEach(p => {
        const src = path.join(ROOT_DIR, p.source);
        const target = p.path ? path.join(ROOT_DIR, lang.code, p.path, 'index.html') : path.join(ROOT_DIR, lang.code, 'index.html');
        if (fs.existsSync(src)) {
            generateLocalizedFile(src, target, lang, p.key, p.path);
        }
    });
});

console.log('\n=== Step 3: Updating XML Sitemap ===');
const sitemapPath = path.join(ROOT_DIR, 'sitemap.xml');
if (fs.existsSync(sitemapPath)) {
    let sitemap = fs.readFileSync(sitemapPath, 'utf8');
    if (!sitemap.includes('xmlns:xhtml=')) {
        sitemap = sitemap.replace('<urlset ', '<urlset xmlns:xhtml="http://www.w3.org/1999/xhtml" ');
    }

    let newEntries = '';
    const today = '2026-09-17';

    PAGES.forEach(p => {
        const trailing = p.path ? (p.path.endsWith('/') ? p.path : p.path + '/') : '';
        LANGS.forEach(l => {
            const locUrl = 'https://auratoolkit360.com/' + l.code + '/' + trailing;
            if (!sitemap.includes('<loc>' + locUrl + '</loc>')) {
                newEntries += '    <url>\n' +
                              '        <loc>' + locUrl + '</loc>\n' +
                              '        <xhtml:link rel="alternate" hreflang="x-default" href="https://auratoolkit360.com/' + trailing + '"/>\n' +
                              '        <xhtml:link rel="alternate" hreflang="en" href="https://auratoolkit360.com/' + trailing + '"/>\n' +
                              LANGS.map(alt => '        <xhtml:link rel="alternate" hreflang="' + alt.code + '" href="https://auratoolkit360.com/' + alt.code + '/' + trailing + '"/>').join('\n') + '\n' +
                              '        <lastmod>' + today + '</lastmod>\n' +
                              '        <changefreq>weekly</changefreq>\n' +
                              '        <priority>' + (p.path === '' ? '1.0' : '0.9') + '</priority>\n' +
                              '    </url>\n';
            }
        });
    });

    if (newEntries) {
        sitemap = sitemap.replace('</urlset>', newEntries + '</urlset>');
        fs.writeFileSync(sitemapPath, sitemap, 'utf8');
        console.log('Updated sitemap.xml with multilingual hreflang URLs!');
    } else {
        console.log('Sitemap already up to date.');
    }
}

console.log('\nAll International SEO and Multilingual Localization tasks completed successfully!');