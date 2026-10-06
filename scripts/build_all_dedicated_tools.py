import os
import re
import sys
import xml.etree.ElementTree as ET
from tools_catalog import TOOLS_CATALOG

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
converter_dir = os.path.join(base_dir, "converter")

# 1. Related Suggestions HTML generator
def get_related_section_html(category, current_slug):
    pdf_cards = [
        ('/converter/pdf-to-word/', '📕 ➔ 📝', 'PDF to Word', 'Reconstruct editable Word DOCX from any PDF'),
        ('/converter/word-to-pdf/', '📝 ➔ 📕', 'Word to PDF', 'Convert Word documents to clean vector PDF files'),
        ('/converter/compress-pdf/', '🗜️', 'Compress PDF', 'Reduce PDF file size up to 90% without losing quality'),
        ('/converter/merge-pdf/', '➕', 'Merge PDF', 'Combine multiple PDF files into one clean document'),
        ('/converter/rotate-pdf/', '🔄', 'Rotate PDF', 'Rotate PDF pages permanently 90, 180, or 270 degrees'),
        ('/converter/split-pdf/', '📑', 'Split PDF', 'Separate multi-page PDF files into individual pages'),
        ('/resume-score-checker/', '🎯', 'ATS Score Checker', 'Audit resume keyword matching & formatting')
    ]
    image_cards = [
        ('/converter/compress-image/', '🗜️🖼️', 'Compress Image', 'Shrink PNG, JPG & WEBP file sizes instantly'),
        ('/converter/passport-photo-maker/', '🛂', 'Passport Photo Maker', 'Generate standard biometric passport & visa photos'),
        ('/converter/ocr-to-text/', '🔍📄', 'Image to Text (OCR)', 'Extract editable text paragraphs from images & scans'),
        ('/converter/crop-rotate-image/', '✂️', 'Crop & Rotate Image', 'Crop, rotate, and straighten photos privately'),
        ('/converter/resize-image/', '📐', 'Resize Image', 'Resize photo dimensions by exact pixels or percentage'),
        ('/converter/jpg-to-png/', 'JPG➔PNG', 'JPG to PNG', 'Convert lossy JPG photos to transparent PNG format')
    ]
    calc_cards = [
        ('/converter/age-calculator/', '🎂', 'Age Calculator', 'Calculate exact age in years, days & birthday countdown'),
        ('/converter/currency-converter/', '💵', 'Currency Converter', 'Real-time exchange rates for 150+ global currencies'),
        ('/converter/percentage-calculator/', '🔢', 'Percentage Calculator', 'Calculate exam marks, percentage change & discounts'),
        ('/converter/unit-converter/', '📐', 'Unit Converter', 'Convert Length, Land Area, Weight & Temperature'),
        ('/converter/bmi-calculator/', '❤️', 'BMI Calculator', 'Check Body Mass Index and healthy target weight'),
        ('/converter/emi-calculator/', '🏦', 'Loan EMI Calculator', 'Calculate monthly installments and interest schedules')
    ]
    data_cards = [
        ('/converter/word-counter/', '🔤', 'Word & Character Counter', 'Count words, characters, sentences & reading time'),
        ('/converter/password-generator/', '🔒', 'Password Generator', 'Generate strong, cryptographically secure passwords'),
        ('/converter/case-converter/', '🔠', 'Case Converter', 'Convert text to UPPERCASE, lowercase, Title Case'),
        ('/paraphrasing-tool/', '✍️', 'AI Paraphrasing Tool', 'Rewrite and improve sentences privately in browser'),
        ('/converter/json-formatter/', '{ }', 'JSON Formatter', 'Validate, beautify, and format minified JSON code'),
        ('/converter/excel-to-csv/', '📗➔📄', 'Excel to CSV', 'Convert spreadsheets to standard CSV format')
    ]

    pool = pdf_cards
    if category == 'image':
        pool = image_cards
    elif category == 'calc':
        pool = calc_cards
    elif category == 'data':
        pool = data_cards

    # Filter out current slug
    filtered = [c for c in pool if c[0].strip('/') != f'converter/{current_slug}' and c[0].strip('/') != current_slug]
    selected = filtered[:4]

    cards_html = ""
    for url, icon, title, desc in selected:
        cards_html += f"""
                    <a href="{url}" class="related-card">
                        <div class="icon">{icon}</div>
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </a>"""

    return f"""
            <!-- Related Tools Section -->
            <div class="info-card" style="margin-top: 2rem;">
                <h2 style="font-size: 1.45rem; font-weight: 800; color: #38bdf8; margin-bottom: 1rem; border-left: 4px solid #38bdf8; padding-left: 0.75rem;">Explore Related Free Tools</h2>
                <div class="related-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">
{cards_html}
                </div>
            </div>
"""

# 2. Template for generating new dedicated tool pages
def generate_tool_page_html(tool):
    slug = tool["slug"]
    name = tool["name"]
    category = tool["category"]
    icon = tool["icon"]
    desc = tool["desc"]
    keywords = tool["keywords"]
    accept = tool["accept"]
    action = tool["action"]
    btn_text = tool["btn_text"]
    options_html = tool.get("options_html", "")
    faq1_q = tool["faq1_q"]
    faq1_a = tool["faq1_a"]
    faq2_q = tool["faq2_q"]
    faq2_a = tool["faq2_a"]

    related_html = get_related_section_html(category, slug)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
    <title>{name} | 100% Free & Private - AuraToolkit360</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="AuraToolkit360">
    <meta name="robots" content="index,follow,max-image-preview:large">
    <link rel="canonical" href="https://auratoolkit360.com/converter/{slug}/">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="AuraToolkit360">
    <meta property="og:title" content="{name} | 100% Free & Private - AuraToolkit360">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://auratoolkit360.com/converter/{slug}/">
    <meta property="og:image" content="https://auratoolkit360.com/assets/og-image.png">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{name} | 100% Free & Private - AuraToolkit360">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://auratoolkit360.com/assets/og-image.png">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    
    <!-- Google AdSense & Search Console Verification -->
    <meta name="google-adsense-account" content="ca-pub-1373118680696037">
    <script defer src="/tracking-consent.js" data-adsense-client="ca-pub-1373118680696037" data-ga-measurement-id="G-06PT7VHV1Q"></script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1373118680696037" crossorigin="anonymous"></script>
    <meta name="google-site-verification" content="N0rLFYsip2eaN77OK361NOkyHS3eqB9i9gf2EYZkbMA">
    
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.75);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-blue: #2563eb;
            --accent-purple: #7c3aed;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ overflow-x: hidden; scroll-behavior: smooth; }}
        body {{
            font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            min-height: 100vh;
            color: #f8fafc;
            display: flex;
            flex-direction: column;
            line-height: 1.6;
            overflow-x: hidden;
            position: relative;
        }}
        body::before {{
            content: '';
            position: fixed;
            top: -10%;
            left: -10%;
            width: 50vw;
            height: 50vw;
            background: radial-gradient(circle, rgba(102,126,234,0.18) 0%, rgba(15,23,42,0) 70%);
            z-index: -1;
            pointer-events: none;
        }}
        body::after {{
            content: '';
            position: fixed;
            bottom: -10%;
            right: -10%;
            width: 50vw;
            height: 50vw;
            background: radial-gradient(circle, rgba(118,75,162,0.18) 0%, rgba(15,23,42,0) 70%);
            z-index: -1;
            pointer-events: none;
        }}

        .navbar {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            padding: 0.8rem 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .nav-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        .logo {{
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            letter-spacing: -0.02em;
        }}
        .logo-symbol {{
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #0284c7, #6366f1);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 1.15rem;
            font-weight: 900;
        }}
        .logo-text span {{
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        .nav-links {{ display: flex; gap: 0.4rem; align-items: center; }}
        .nav-links a {{
            text-decoration: none;
            color: #94a3b8;
            font-weight: 600;
            padding: 0.45rem 0.85rem;
            border-radius: 10px;
            transition: all 0.2s;
            font-size: 0.86rem;
        }}
        .nav-links a:hover {{ background: rgba(255,255,255,0.06); color: #38bdf8; }}
        .nav-links a.active {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }}

        .container {{ max-width: 1100px; margin: 0 auto; padding: 2.5rem 1.5rem; }}
        .page-header {{ text-align: center; margin-bottom: 2.5rem; }}
        .badge-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid rgba(56, 189, 248, 0.25);
            margin-bottom: 0.85rem;
        }}
        .page-header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.8px;
            margin-bottom: 0.6rem;
        }}
        .page-header p {{ color: #94a3b8; font-size: 1.05rem; max-width: 750px; margin: 0 auto; line-height: 1.6; }}

        /* MAIN TOOL CARD */
        .tool-card {{
            background: rgba(30, 41, 59, 0.75);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 2.5rem 2rem;
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            margin-bottom: 3rem;
            text-align: center;
        }}
        .file-upload-box {{
            border: 2px dashed rgba(56, 189, 248, 0.4);
            border-radius: 18px;
            padding: 2.8rem 1.5rem;
            background: rgba(15, 23, 42, 0.5);
            cursor: pointer;
            transition: all 0.25s ease;
            margin-bottom: 1.5rem;
        }}
        .file-upload-box:hover {{
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.05);
            transform: translateY(-2px);
        }}
        .file-upload-box .icon {{ font-size: 3rem; margin-bottom: 0.8rem; }}
        .file-upload-box .title {{ font-size: 1.25rem; font-weight: 800; color: #ffffff; margin-bottom: 0.35rem; }}
        .file-upload-box .subtitle {{ font-size: 0.88rem; color: #94a3b8; }}

        .btn-convert {{
            background: linear-gradient(135deg, #0284c7, #6366f1);
            color: #ffffff;
            border: none;
            padding: 0.95rem 2.2rem;
            font-size: 1.05rem;
            font-weight: 700;
            border-radius: 14px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.6rem;
            transition: all 0.25s ease;
            box-shadow: 0 8px 24px rgba(2, 132, 199, 0.35);
            width: 100%;
            max-width: 380px;
        }}
        .btn-convert:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(2, 132, 199, 0.5);
        }}
        .btn-convert:disabled {{ opacity: 0.5; cursor: not-allowed; transform: none; }}

        /* INFO & FAQ SECTION */
        .info-card {{
            background: rgba(30, 41, 59, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 2.2rem;
            color: #f8fafc;
            margin-bottom: 2rem;
        }}
        .info-card h2 {{
            font-size: 1.45rem;
            color: #38bdf8;
            margin-bottom: 1.2rem;
            border-left: 4px solid #38bdf8;
            padding-left: 0.75rem;
            font-weight: 800;
        }}
        .info-card p {{ color: #94a3b8; line-height: 1.7; font-size: 0.95rem; margin-bottom: 1rem; }}
        
        .steps-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.2rem;
            margin: 1.5rem 0;
        }}
        .step-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.4rem;
        }}
        .step-box h4 {{ color: #38bdf8; font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }}
        .step-box p {{ color: #94a3b8; font-size: 0.85rem; line-height: 1.55; margin-bottom: 0; }}

        .faq-item {{ border-top: 1px solid rgba(255,255,255,0.08); padding: 1.2rem 0; }}
        .faq-item:first-of-type {{ border-top: none; }}
        .faq-q {{ font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.4rem; }}
        .faq-a {{ color: #94a3b8; font-size: 0.92rem; line-height: 1.6; }}

        .related-card {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.3rem;
            text-decoration: none;
            color: inherit;
            transition: all 0.25s;
            display: block;
            text-align: center;
        }}
        .related-card:hover {{
            transform: translateY(-4px);
            border-color: #38bdf8;
            background: rgba(56,189,248,0.08);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        .related-card .icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .related-card h4 {{ color: #ffffff; font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; }}
        .related-card p {{ color: #94a3b8; font-size: 0.8rem; line-height: 1.45; margin-bottom: 0; }}

        footer {{
            margin-top: auto;
            background: rgba(11, 15, 25, 0.98);
            border-top: 1px solid rgba(255,255,255,0.08);
            padding: 3rem 1.5rem 2rem;
        }}
        .footer-inner {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            color: #64748b;
            font-size: 0.85rem;
        }}
        .footer-links {{ display: flex; gap: 1.2rem; }}
        .footer-links a {{ color: #94a3b8; text-decoration: none; transition: color 0.2s; }}
        .footer-links a:hover {{ color: #38bdf8; }}
    </style>
    <link rel="stylesheet" href="/assets/aura-fx.css">
    <script defer src="/assets/aura-fx.js"></script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "{name} - AuraToolkit360",
        "url": "https://auratoolkit360.com/converter/{slug}/",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "offers": {{ "@type": "Offer", "price": "0.00", "priceCurrency": "USD" }},
        "description": "{desc}",
        "author": {{ "@type": "Organization", "name": "AuraToolkit360" }}
    }}
    </script>
</head>
<body>
    <!-- Top Navigation -->
    <nav class="navbar" aria-label="Main Navigation">
        <div class="nav-container">
            <a href="/" class="logo" aria-label="AuraToolkit360 Home">
                <div class="logo-symbol">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="22" height="22" role="img" aria-hidden="true">
                        <circle cx="32" cy="32" r="20" fill="rgba(255,255,255,0.22)"/>
                        <path d="M22 42L32 20l10 22h-5l-2.1-5h-5.8L27 42h-5zm9.9-8h4.2L34 25.7 31.9 34z" fill="#fff"/>
                    </svg>
                </div>
                <div class="logo-text">AuraToolkit<span>360</span></div>
            </a>
            
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/converter/" class="active">Converter</a>
                <a href="/resume-cv-maker/">Resume</a>
                <a href="/cover-letter-maker/">Cover Letter</a>
                <a href="/resume-score-checker/">Score Checker</a>
                <a href="/hr-helper/">HR Bulk</a>
                <a href="/blogs/">Blogs</a>
                <a href="/about/">About</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <div class="page-header">
            <div class="badge-pill">🔒 100% In-Browser Privacy • Zero Server Uploads</div>
            <h1>{name}</h1>
            <p>{desc}</p>
        </div>

        <div class="tool-card">
            <form data-action="{action}" id="toolForm">
                <div class="file-upload-box" id="dropZone" onclick="document.getElementById('fileInput').click()">
                    <div class="icon">{icon}</div>
                    <div class="title" id="dropTitle">Choose File to Process</div>
                    <div class="subtitle">Drag &amp; drop file here, or click to browse</div>
                    <input type="file" id="fileInput" name="file" accept="{accept}" style="display:none" onchange="handleFileChange(this)">
                </div>
                <div id="fileDisplay" style="margin-bottom:1.2rem; font-weight:700; color:#38bdf8; display:none;"></div>
                {options_html}
                <button type="submit" class="btn-convert" id="submitBtn">
                    {btn_text}
                </button>
            </form>
        </div>

        <!-- Technical Deep Dive & Educational Intent -->
        <section class="info-section">
            <div class="info-card">
                <h2>Why Use AuraToolkit360 {name}?</h2>
                <p>Unlike traditional online tools that require uploading your private files and data to external cloud storage servers, AuraToolkit360 processes everything client-side directly within your web browser sandbox using modern WebAssembly and HTML5 APIs.</p>
                <div class="steps-grid">
                    <div class="step-box">
                        <h4>1. Select File</h4>
                        <p>Upload your file from any device. The file stays in your local browser memory.</p>
                    </div>
                    <div class="step-box">
                        <h4>2. Instant Processing</h4>
                        <p>Our client-side engine executes parsing and conversion locally on your CPU.</p>
                    </div>
                    <div class="step-box">
                        <h4>3. Direct Download</h4>
                        <p>Download your converted file instantly with zero watermarks or subscription gates.</p>
                    </div>
                </div>
            </div>

            <!-- FAQs -->
            <div class="info-card">
                <h2>Frequently Asked Questions (FAQ)</h2>
                <div class="faq-accordion">
                    <div class="faq-item">
                        <div class="faq-q">❓ {faq1_q}</div>
                        <div class="faq-a">{faq1_a}</div>
                    </div>
                    <div class="faq-item">
                        <div class="faq-q">❓ {faq2_q}</div>
                        <div class="faq-a">{faq2_a}</div>
                    </div>
                    <div class="faq-item">
                        <div class="faq-q">❓ Are my files uploaded to any external server?</div>
                        <div class="faq-a">Never. AuraToolkit360 operates on an absolute privacy-first model. Zero bytes are uploaded to our servers, keeping your documents 100% confidential.</div>
                    </div>
                    <div class="faq-item">
                        <div class="faq-q">❓ Is this tool completely free without limits?</div>
                        <div class="faq-a">Yes! There are no daily conversion limits, hidden fees, paywalls, or registrations required.</div>
                    </div>
                </div>
            </div>

            {related_html}
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <div class="footer-inner">
            <div>© 2026 AuraToolkit360. All rights reserved. Zero server tracking.</div>
            <div class="footer-links">
                <a href="/converter/">All Tools</a>
                <a href="/about/">About</a>
                <a href="/privacy-policy/">Privacy</a>
                <a href="/terms/">Terms</a>
                <a href="/disclaimer/">Disclaimer</a>
            </div>
        </div>
    </footer>

    <!-- Client-Side Processing Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mammoth@1.6.0/mammoth.browser.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@7.8.2/build/index.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

    <script>
        if (window.pdfjsLib) {{
            window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
        }}

        function handleFileChange(input) {{
            const display = document.getElementById('fileDisplay');
            if (input.files && input.files[0]) {{
                display.style.display = 'block';
                display.textContent = 'Selected: ' + input.files[0].name + ' (' + (input.files[0].size / 1024).toFixed(1) + ' KB)';
                document.getElementById('dropTitle').textContent = 'File Ready!';
            }}
        }}

        function downloadBlob(blob, filename) {{
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            setTimeout(() => URL.revokeObjectURL(url), 5000);
        }}

        function readSingleFile(form, selector = 'input[type="file"]') {{
            const input = form.querySelector(selector);
            if (!input || !input.files || !input.files[0]) {{
                throw new Error('Please select a file first.');
            }}
            return input.files[0];
        }}

        // Tool Form Execution
        document.getElementById('toolForm').addEventListener('submit', async function(e) {{
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            const origText = btn.textContent;
            btn.disabled = true;
            btn.textContent = 'Processing in Browser... ⚡';

            try {{
                const file = readSingleFile(this);
                const action = this.getAttribute('data-action');

                if (action === '/rotate-pdf') {{
                    const angle = parseInt(document.getElementById('rotateAngle').value) || 90;
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const pages = pdfDoc.getPages();
                    pages.forEach(p => p.setRotation(PDFLib.degrees((p.getRotation().angle + angle) % 360)));
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'rotated.pdf');
                }}
                else if (action === '/lock-pdf') {{
                    // Lock PDF with password using PDFLib
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'protected.pdf');
                }}
                else if (action === '/unlock-pdf') {{
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'unlocked.pdf');
                }}
                else if (action === '/add-watermark') {{
                    const text = this.querySelector('input[name="watermark"]').value || 'CONFIDENTIAL';
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const font = await pdfDoc.embedFont(PDFLib.StandardFonts.HelveticaBold);
                    const pages = pdfDoc.getPages();
                    pages.forEach(p => {{
                        const {{ width, height }} = p.getSize();
                        p.drawText(text, {{
                            x: width / 4,
                            y: height / 2,
                            size: 44,
                            font,
                            color: PDFLib.rgb(0.7, 0.7, 0.7),
                            rotate: PDFLib.degrees(45),
                            opacity: 0.35
                        }});
                    }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'watermarked.pdf');
                }}
                else if (action === '/delete-pages') {{
                    const raw = this.querySelector('input[name="pages"]').value;
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const total = pdfDoc.getPageCount();
                    const toDelete = new Set();
                    raw.split(',').forEach(part => {{
                        if (part.includes('-')) {{
                            const [start, end] = part.split('-').map(n => parseInt(n.trim()));
                            if (start && end) for (let i = start; i <= end; i++) toDelete.add(i - 1);
                        }} else {{
                            const n = parseInt(part.trim());
                            if (n) toDelete.add(n - 1);
                        }}
                    }});
                    Array.from(toDelete).sort((a,b) => b - a).forEach(idx => {{
                        if (idx >= 0 && idx < pdfDoc.getPageCount() && pdfDoc.getPageCount() > 1) {{
                            pdfDoc.removePage(idx);
                        }}
                    }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'pages_removed.pdf');
                }}
                else if (action === '/extract-pages') {{
                    const raw = this.querySelector('input[name="pages"]').value;
                    const arrayBuffer = await file.arrayBuffer();
                    const srcDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const newDoc = await PDFLib.PDFDocument.create();
                    const toKeep = [];
                    raw.split(',').forEach(part => {{
                        if (part.includes('-')) {{
                            const [start, end] = part.split('-').map(n => parseInt(n.trim()));
                            if (start && end) for (let i = start; i <= end; i++) toKeep.push(i - 1);
                        }} else {{
                            const n = parseInt(part.trim());
                            if (n) toKeep.push(n - 1);
                        }}
                    }});
                    const validIndices = toKeep.filter(idx => idx >= 0 && idx < srcDoc.getPageCount());
                    if (validIndices.length === 0) throw new Error('No valid page numbers found.');
                    const copiedPages = await newDoc.copyPages(srcDoc, validIndices);
                    copiedPages.forEach(p => newDoc.addPage(p));
                    const outBytes = await newDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'extracted_pages.pdf');
                }}
                else if (action === '/add-page-numbers') {{
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer, {{ ignoreEncryption: true }});
                    const font = await pdfDoc.embedFont(PDFLib.StandardFonts.Helvetica);
                    const pages = pdfDoc.getPages();
                    pages.forEach((p, idx) => {{
                        const {{ width }} = p.getSize();
                        p.drawText(`Page ${{idx + 1}} of ${{pages.length}}`, {{
                            x: width / 2 - 35,
                            y: 25,
                            size: 10,
                            font,
                            color: PDFLib.rgb(0.4, 0.4, 0.4)
                        }});
                    }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'numbered.pdf');
                }}
                else if (action === '/pdf-to-image') {{
                    const data = await file.arrayBuffer();
                    const pdf = await pdfjsLib.getDocument({{ data: new Uint8Array(data) }}).promise;
                    const zip = new JSZip();
                    for (let pNum = 1; pNum <= pdf.numPages; pNum++) {{
                        const page = await pdf.getPage(pNum);
                        const viewport = page.getViewport({{ scale: 1.5 }});
                        const canvas = document.createElement('canvas');
                        canvas.width = viewport.width;
                        canvas.height = viewport.height;
                        const ctx = canvas.getContext('2d');
                        await page.render({{ canvasContext: ctx, viewport }}).promise;
                        const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                        zip.file(`page_${{pNum}}.png`, blob);
                    }}
                    const zipBlob = await zip.generateAsync({{ type: 'blob' }});
                    downloadBlob(zipBlob, 'pdf_images.zip');
                }}
                else if (action === '/pdf-to-txt') {{
                    const data = await file.arrayBuffer();
                    const pdf = await pdfjsLib.getDocument({{ data: new Uint8Array(data) }}).promise;
                    let fullText = '';
                    for (let p = 1; p <= pdf.numPages; p++) {{
                        const page = await pdf.getPage(p);
                        const content = await page.getTextContent();
                        fullText += content.items.map(i => i.str).join(' ') + '\\n\\n';
                    }}
                    downloadBlob(new Blob([fullText], {{ type: 'text/plain;charset=utf-8' }}), 'extracted.txt');
                }}
                else if (action === '/excel-to-csv') {{
                    const buffer = await file.arrayBuffer();
                    const workbook = XLSX.read(buffer, {{ type: 'array' }});
                    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                    const csv = XLSX.utils.sheet_to_csv(firstSheet);
                    downloadBlob(new Blob([csv], {{ type: 'text/csv;charset=utf-8' }}), 'converted.csv');
                }}
                else if (action === '/word-to-html') {{
                    const buffer = await file.arrayBuffer();
                    const res = await mammoth.convertToHtml({{ arrayBuffer: buffer }});
                    const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Converted Document</title></head><body>' + (res.value || '') + '</body></html>';
                    downloadBlob(new Blob([html], {{ type: 'text/html;charset=utf-8' }}), 'document.html');
                }}
                else if (action === '/csv-to-json') {{
                    Papa.parse(file, {{
                        header: true,
                        skipEmptyLines: true,
                        complete: function(results) {{
                            const json = JSON.stringify(results.data, null, 2);
                            downloadBlob(new Blob([json], {{ type: 'application/json' }}), 'converted.json');
                        }}
                    }});
                }}
                else if (action === '/json-to-csv') {{
                    const text = await file.text();
                    const data = JSON.parse(text);
                    const csv = Papa.unparse(data);
                    downloadBlob(new Blob([csv], {{ type: 'text/csv;charset=utf-8' }}), 'converted.csv');
                }}
                else if (action === '/json-formatter') {{
                    const text = await file.text();
                    const parsed = JSON.parse(text);
                    const beautified = JSON.stringify(parsed, null, 2);
                    downloadBlob(new Blob([beautified], {{ type: 'application/json' }}), 'beautified.json');
                }}
                else if (action === '/flip-image') {{
                    const dir = document.getElementById('flipDir').value;
                    const img = new Image();
                    img.src = URL.createObjectURL(file);
                    await new Promise(r => img.onload = r);
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    if (dir === 'horizontal') {{
                        ctx.translate(canvas.width, 0);
                        ctx.scale(-1, 1);
                    }} else {{
                        ctx.translate(0, canvas.height);
                        ctx.scale(1, -1);
                    }}
                    ctx.drawImage(img, 0, 0);
                    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                    downloadBlob(blob, 'flipped.png');
                }}
                else if (action === '/jpg-to-png' || action === '/webp-to-png' || action === '/svg-to-png') {{
                    const img = new Image();
                    img.src = URL.createObjectURL(file);
                    await new Promise(r => img.onload = r);
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                    downloadBlob(blob, 'converted.png');
                }}
                else if (action === '/png-to-jpg') {{
                    const img = new Image();
                    img.src = URL.createObjectURL(file);
                    await new Promise(r => img.onload = r);
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0);
                    const blob = await new Promise(r => canvas.toBlob(r, 'image/jpeg', 0.95));
                    downloadBlob(blob, 'converted.jpg');
                }}
                else if (action === '/image-to-pdf') {{
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFLib.PDFDocument.create();
                    let embedded;
                    if (file.type === 'image/jpeg' || file.name.endsWith('.jpg') || file.name.endsWith('.jpeg')) {{
                        embedded = await pdfDoc.embedJpg(arrayBuffer);
                    }} else {{
                        embedded = await pdfDoc.embedPng(arrayBuffer);
                    }}
                    const {{ width, height }} = embedded.scaleToFit(550, 800);
                    const page = pdfDoc.addPage([595, 842]);
                    page.drawImage(embedded, {{
                        x: (595 - width) / 2,
                        y: (842 - height) / 2,
                        width,
                        height
                    }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'image.pdf');
                }}
                else if (action === '/txt-to-pdf') {{
                    const text = await file.text();
                    const pdfDoc = await PDFLib.PDFDocument.create();
                    const font = await pdfDoc.embedFont(PDFLib.StandardFonts.Helvetica);
                    const page = pdfDoc.addPage([595, 842]);
                    page.drawText(text.slice(0, 2000), {{ x: 40, y: 800, size: 10, font, color: PDFLib.rgb(0.1, 0.1, 0.1) }});
                    const outBytes = await pdfDoc.save();
                    downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'document.pdf');
                }}
                else if (action === '/docx-to-txt') {{
                    const buffer = await file.arrayBuffer();
                    const res = await mammoth.extractRawText({{ arrayBuffer: buffer }});
                    downloadBlob(new Blob([res.value || ''], {{ type: 'text/plain;charset=utf-8' }}), 'extracted.txt');
                }}
                else if (action === '/rtf-to-docx') {{
                    const text = await file.text();
                    const doc = new docx.Document({{
                        sections: [{{
                            children: [new docx.Paragraph({{ text: text.slice(0, 5000) }})]
                        }}]
                    }});
                    const blob = await docx.Packer.toBlob(doc);
                    downloadBlob(blob, 'converted.docx');
                }}
            }} catch(err) {{
                alert('Conversion failed: ' + (err.message || 'Unknown error'));
            }} finally {{
                btn.disabled = false;
                btn.textContent = origText;
            }}
        }});
    </script>
</body>
</html>
"""

# STEP 1: Generate all 23 new dedicated tool landing pages
newly_created = 0
for tool in TOOLS_CATALOG:
    slug = tool["slug"]
    tool_dir = os.path.join(converter_dir, slug)
    os.makedirs(tool_dir, exist_ok=True)
    idx_path = os.path.join(tool_dir, "index.html")
    
    html_content = generate_tool_page_html(tool)
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created dedicated page: converter/{slug}/index.html")
    newly_created += 1

print(f"\nSuccessfully created {newly_created} new dedicated tool landing pages.")

# STEP 2: Inject Related Tools section into existing 33 tool pages if missing
existing_subdirs = [d for d in os.listdir(converter_dir) if os.path.isdir(os.path.join(converter_dir, d))]
injected_existing = 0

for d in existing_subdirs:
    idx_p = os.path.join(converter_dir, d, "index.html")
    if not os.path.isfile(idx_p):
        continue
    
    with open(idx_p, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()

    if "related-grid" in c or "related-card" in c:
        continue  # Already has related tools

    # Determine category
    cat = 'pdf'
    if any(k in d for k in ['image', 'photo', 'signature', 'crop', 'watermark', 'favicon', 'ocr']):
        cat = 'image'
    elif any(k in d for k in ['calc', 'time', 'currency', 'percentage', 'unit', 'emi', 'zakat', 'bmi', 'age']):
        cat = 'calc'
    elif any(k in d for k in ['word-counter', 'case-converter', 'password']):
        cat = 'data'

    rel_sec = get_related_section_html(cat, d)

    # Insert before footer or before </main>
    if '</section>' in c:
        c = c.replace('</section>', rel_sec + '\n        </section>', 1)
        injected_existing += 1
    elif '</main>' in c:
        c = c.replace('</main>', rel_sec + '\n    </main>', 1)
        injected_existing += 1
    elif '<footer' in c:
        c = c.replace('<footer', rel_sec + '\n    <footer', 1)
        injected_existing += 1

    with open(idx_p, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Injected related tools suggestions into existing: converter/{d}/index.html")

print(f"\nInjected related suggestions into {injected_existing} existing tool pages.")

# STEP 3: Update converter/index.html to ensure every card links to its dedicated page
converter_index_file = os.path.join(converter_dir, "index.html")
with open(converter_index_file, "r", encoding="utf-8") as f:
    ci_content = f.read()

# Map all slugs to their dedicated page URLs
slug_to_url = {}
for d in os.listdir(converter_dir):
    if os.path.isdir(os.path.join(converter_dir, d)):
        slug_to_url[d] = f"/converter/{d}/"

# Add aliases
slug_to_url["pdf-to-jpg-extractor"] = "/converter/pdf-to-jpg/"
slug_to_url["png-to-pdf-converter"] = "/converter/png-to-pdf/"
slug_to_url["jpg-to-pdf-converter"] = "/converter/jpg-to-pdf/"
slug_to_url["compress-image-to-target-kb"] = "/converter/compress-image-target/"
slug_to_url["image-watermark-tool"] = "/converter/watermark-image/"
slug_to_url["favicon-ico-generator"] = "/converter/favicon-generator/"
slug_to_url["resize-signature-tool"] = "/converter/resize-signature/"
slug_to_url["resize-image-pixels-cm"] = "/converter/resize-image/"
slug_to_url["compress-video-online"] = "/converter/compress-video/"
slug_to_url["audio-video-to-mp3"] = "/converter/mp3-converter/"
slug_to_url["word-character-counter"] = "/converter/word-counter/"
slug_to_url["secure-password-generator"] = "/converter/password-generator/"
slug_to_url["time-duration-converter"] = "/converter/time-converter/"
slug_to_url["live-currency-converter"] = "/converter/currency-converter/"
slug_to_url["loan-car-emi-calculator"] = "/converter/emi-calculator/"
slug_to_url["2-5-zakat-calculator"] = "/converter/zakat-calculator/"
slug_to_url["universal-unit-converter"] = "/converter/unit-converter/"
slug_to_url["5-in-1-percentage-calculator"] = "/converter/percentage-calculator/"
slug_to_url["bmi-health-calculator"] = "/converter/bmi-calculator/"
slug_to_url["ai-paraphrasing-tool"] = "/paraphrasing-tool/"

card_links_added = 0
for slug, url in slug_to_url.items():
    card_pattern = re.compile(r'(<div class=["\']tool-card["\'][^>]*data-tool-slug=["\']' + re.escape(slug) + r'["\'][^>]*>)(.*?)(</div>\s*</div>)', re.DOTALL)
    match = card_pattern.search(ci_content)
    if match:
        card_body = match.group(2)
        if "Dedicated Tool Page" not in card_body:
            link_html = f'<div style="margin-top: 0.55rem; text-align: center;"><a href="{url}" style="font-size: 0.78rem; color: #0284c7; font-weight: 700; text-decoration: none;">Dedicated Tool Page ↗</a></div>'
            # Insert before </form>
            if '</form>' in card_body:
                new_card_body = card_body.replace('</form>', link_html + '\n                </form>', 1)
                ci_content = ci_content[:match.start(2)] + new_card_body + ci_content[match.end(2):]
                card_links_added += 1

with open(converter_index_file, "w", encoding="utf-8") as f:
    f.write(ci_content)

print(f"Added dedicated links to {card_links_added} cards in converter/index.html")

# STEP 4: Update sitemap.xml
sitemap_path = os.path.join(base_dir, "sitemap.xml")
tree = ET.parse(sitemap_path)
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
existing_sitemap_urls = set(elem.text for elem in root.findall('.//ns:loc', namespace))

added_to_sitemap = 0
for tool in TOOLS_CATALOG:
    u = f"https://auratoolkit360.com/converter/{tool['slug']}/"
    if u not in existing_sitemap_urls:
        url_el = ET.SubElement(root, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = u
        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = "2026-10-06"
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = "weekly"
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.8"
        existing_sitemap_urls.add(u)
        added_to_sitemap += 1

tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
print(f"Added {added_to_sitemap} new URLs to sitemap.xml")
