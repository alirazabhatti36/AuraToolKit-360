import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

# Catalog of the 23 tools to generate
TOOLS_CATALOG = [
    {
        "slug": "rotate-pdf",
        "name": "Rotate PDF Online",
        "category": "pdf",
        "icon": "🔄📕",
        "desc": "Rotate PDF pages 90, 180, or 270 degrees clockwise or counterclockwise. Permanent orientation correction in your browser.",
        "keywords": "rotate pdf online, rotate pdf pages, turn pdf upside down, fix pdf orientation, free pdf rotator",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/rotate-pdf",
        "btn_text": "Rotate PDF Pages ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Rotation Angle:</label>
                <select id="rotateAngle" style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
                    <option value="90">90° Clockwise</option>
                    <option value="180">180° Half Turn</option>
                    <option value="270">270° (90° Counter-Clockwise)</option>
                </select>
            </div>
        """,
        "faq1_q": "Can I rotate all pages or only specific pages?",
        "faq1_a": "By default, our In-Browser tool rotates all pages uniformly to ensure clean readability across all PDF viewers.",
        "faq2_q": "Will rotating the PDF reduce text quality or compress images?",
        "faq2_a": "No. Rotating alters only the internal page orientation metadata matrix in the PDF stream. Zero loss of vector text sharpness or image fidelity occurs."
    },
    {
        "slug": "lock-pdf",
        "name": "Lock PDF with Password",
        "category": "pdf",
        "icon": "🔒📕",
        "desc": "Protect confidential PDF documents with 128-bit/256-bit encryption and password protection online.",
        "keywords": "lock pdf online, password protect pdf, encrypt pdf free, secure pdf document, add password to pdf",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/lock-pdf",
        "btn_text": "Lock & Encrypt PDF ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Set Password:</label>
                <input type="password" name="password" placeholder="Enter secure password" required style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
            </div>
        """,
        "faq1_q": "Does AuraToolkit360 see or store my password?",
        "faq1_a": "Never. Encryption algorithms run 100% inside your browser using client-side JavaScript. Neither your file nor your password ever leaves your device.",
        "faq2_q": "Can someone open the locked PDF without the password?",
        "faq2_a": "No. Modern PDF viewers (Adobe Acrobat, Chrome, Preview) require the exact password before unlocking the document."
    },
    {
        "slug": "unlock-pdf",
        "name": "Unlock PDF Online",
        "category": "pdf",
        "icon": "🔓📕",
        "desc": "Remove password restrictions and owner security from PDF files you have permissions for.",
        "keywords": "unlock pdf online, remove pdf password, decrypt pdf free, pdf password remover",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/unlock-pdf",
        "btn_text": "Unlock PDF ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Current Password (if known):</label>
                <input type="password" name="password" placeholder="Enter password to decrypt" style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
            </div>
        """,
        "faq1_q": "How does unlocking work?",
        "faq1_a": "When you provide the authorization password, the tool decrypts the binary stream in browser memory and saves an unencrypted, open PDF copy.",
        "faq2_q": "Is this safe for sensitive contracts?",
        "faq2_a": "Yes! Because no files are uploaded to any cloud server, your sensitive business contracts remain strictly on your computer."
    },
    {
        "slug": "add-watermark",
        "name": "Add Watermark to PDF",
        "category": "pdf",
        "icon": "💧📕",
        "desc": "Stamp confidential text watermarks like DRAFT, CONFIDENTIAL, or your company name across all PDF pages.",
        "keywords": "add watermark to pdf, stamp pdf online, confidential watermark pdf, free pdf watermark maker",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/add-watermark",
        "btn_text": "Apply Watermark & Download ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Watermark Text:</label>
                <input type="text" name="watermark" placeholder="e.g. CONFIDENTIAL or DRAFT" required style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
            </div>
        """,
        "faq1_q": "Can the watermark text be customized?",
        "faq1_a": "Yes! You can enter any custom phrase, such as 'CONFIDENTIAL', 'SAMPLE', 'COPY', or your brand name.",
        "faq2_q": "Where does the watermark appear on the page?",
        "faq2_a": "It is rendered diagonally across the center of every page in semi-transparent light grey so it remains visible without obstructing underlying text."
    },
    {
        "slug": "delete-pages",
        "name": "Delete Pages from PDF",
        "category": "pdf",
        "icon": "🗑️📕",
        "desc": "Remove unwanted or blank pages from any PDF document quickly and download a cleaned copy.",
        "keywords": "delete pages from pdf, remove pdf pages online, drop page from pdf, free pdf page remover",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/delete-pages",
        "btn_text": "Remove Pages & Download ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Pages to remove (e.g. 1, 3, 5-7):</label>
                <input type="text" name="pages" placeholder="e.g. 1, 3, 5-7" required style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
            </div>
        """,
        "faq1_q": "How do I specify multiple pages?",
        "faq1_a": "You can use comma separation (e.g. 1, 4, 8) or hyphen ranges (e.g. 3-6) to remove multiple pages in one go.",
        "faq2_q": "Does deleting pages alter the remaining pages?",
        "faq2_a": "No. All remaining pages retain 100% of their original fonts, vector formatting, and image resolution."
    },
    {
        "slug": "extract-pages",
        "name": "Extract Pages from PDF",
        "category": "pdf",
        "icon": "✂️📕",
        "desc": "Extract specific pages from a large PDF and save them as a clean new standalone PDF file.",
        "keywords": "extract pages from pdf, separate pages from pdf, export pdf page range, save specific pdf pages",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/extract-pages",
        "btn_text": "Extract Pages & Download ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Pages to keep (e.g. 1-3, 5):</label>
                <input type="text" name="pages" placeholder="e.g. 1-3, 5" required style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
            </div>
        """,
        "faq1_q": "How is Extract different from Delete?",
        "faq1_a": "Extract creates a new PDF containing ONLY the exact page numbers you specify, discarding everything else.",
        "faq2_q": "Is there a limit on how many pages I can extract?",
        "faq2_a": "No limit. Because processing occurs directly in your browser's memory, you can extract 1 page or 100 pages freely."
    },
    {
        "slug": "add-page-numbers",
        "name": "Add Page Numbers to PDF",
        "category": "pdf",
        "icon": "🔢📕",
        "desc": "Number PDF pages automatically at the bottom center of each page for professional document organization.",
        "keywords": "add page numbers to pdf, number pdf pages online, paginate pdf free, insert page numbers pdf",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/add-page-numbers",
        "btn_text": "Add Page Numbers & Download ⚡",
        "options_html": "",
        "faq1_q": "Where are the page numbers placed?",
        "faq1_a": "They are placed neatly at the bottom center of each page, formatted as 'Page X of Y' for executive presentation.",
        "faq2_q": "Does this support multi-page documents?",
        "faq2_a": "Yes! Whether your PDF is 2 pages or 200 pages, page numbers are calculated and embedded automatically."
    },
    {
        "slug": "pdf-to-image",
        "name": "Convert PDF to Image (PNG)",
        "category": "pdf",
        "icon": "📕➔🖼️",
        "desc": "Convert PDF pages into high-resolution PNG images online for free. 100% private in-browser rendering.",
        "keywords": "pdf to image online, convert pdf to png, export pdf as pictures, pdf to high res image",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/pdf-to-image",
        "btn_text": "Convert PDF to Images ⚡",
        "options_html": "",
        "faq1_q": "What format are the extracted images?",
        "faq1_a": "Pages are rendered as crisp, lossless PNG images suitable for presentations and web uploads.",
        "faq2_q": "How do I download multiple pages?",
        "faq2_a": "Multi-page documents are automatically bundled and downloaded as a convenient ZIP archive containing all page images."
    },
    {
        "slug": "pdf-to-txt",
        "name": "Convert PDF to Text (TXT)",
        "category": "pdf",
        "icon": "📕➔📄",
        "desc": "Extract clean, unformatted plain text from any PDF document for data processing and analysis.",
        "keywords": "pdf to txt online, extract text from pdf, convert pdf to plain text, parse pdf to text free",
        "input_type": "file",
        "accept": ".pdf",
        "action": "/pdf-to-txt",
        "btn_text": "Extract Text to TXT ⚡",
        "options_html": "",
        "faq1_q": "Does this work on scanned documents?",
        "faq1_a": "For scanned paper documents or photos, please use our companion OCR Image to Text tool which utilizes neural character recognition.",
        "faq2_q": "Is the extracted text clean?",
        "faq2_a": "Yes! It extracts all raw textual strings, paragraphs, and headings cleanly into a lightweight UTF-8 .txt file."
    },
    {
        "slug": "rtf-to-docx",
        "name": "Convert RTF to Word (DOCX)",
        "category": "data",
        "icon": "📄➔📝",
        "desc": "Convert legacy Rich Text Format (.rtf) documents into modern Microsoft Word .docx format.",
        "keywords": "rtf to docx online, convert rtf to word, rich text format to docx, free rtf to word converter",
        "input_type": "file",
        "accept": ".rtf",
        "action": "/rtf-to-docx",
        "btn_text": "Convert RTF to DOCX ⚡",
        "options_html": "",
        "faq1_q": "Why convert RTF to DOCX?",
        "faq1_a": "DOCX is the modern international standard supported by all office suites, applicant tracking systems, and mobile devices.",
        "faq2_q": "Does formatting get preserved?",
        "faq2_a": "Yes! Paragraphs, headings, and bold text are cleanly preserved in the modern Word document."
    },
    {
        "slug": "txt-to-pdf",
        "name": "Convert TXT to PDF",
        "category": "pdf",
        "icon": "📄➔📕",
        "desc": "Convert plain text files (.txt) into formatted, print-ready PDF documents instantly in your browser.",
        "keywords": "txt to pdf online, convert text to pdf, plain text to pdf free, text file to pdf creator",
        "input_type": "file",
        "accept": ".txt",
        "action": "/txt-to-pdf",
        "btn_text": "Convert TXT to PDF ⚡",
        "options_html": "",
        "faq1_q": "How does TXT to PDF format the text?",
        "faq1_a": "It applies clean ISO A4 margins, professional typography (Helvetica), and automatic line wraps for executive presentation.",
        "faq2_q": "Is my text uploaded to a server?",
        "faq2_a": "Never! Everything compiles directly in browser RAM."
    },
    {
        "slug": "docx-to-txt",
        "name": "Convert Word DOCX to TXT",
        "category": "data",
        "icon": "📝➔📄",
        "desc": "Extract raw plain text from Microsoft Word (.docx) files without formatting clutter.",
        "keywords": "docx to txt online, word to text converter, extract plain text from word, word to txt free",
        "input_type": "file",
        "accept": ".docx",
        "action": "/docx-to-txt",
        "btn_text": "Extract Text to TXT ⚡",
        "options_html": "",
        "faq1_q": "What happens to images and tables?",
        "faq1_a": "They are skipped in favor of pure readable paragraph text, ideal for natural language processing, AI training, or text search.",
        "faq2_q": "Can I use this for resumes?",
        "faq2_a": "Yes! Testing how your resume looks as plain text is a great way to verify ATS readability."
    },
    {
        "slug": "excel-to-csv",
        "name": "Convert Excel to CSV",
        "category": "data",
        "icon": "📗➔📄",
        "desc": "Convert Excel spreadsheets (.xlsx, .xls) to clean, standard Comma-Separated Values (.csv) format.",
        "keywords": "excel to csv online, convert xlsx to csv, spreadsheet to csv free, excel sheet to csv",
        "input_type": "file",
        "accept": ".xlsx,.xls",
        "action": "/excel-to-csv",
        "btn_text": "Convert Excel to CSV ⚡",
        "options_html": "",
        "faq1_q": "Does this work on multi-column spreadsheets?",
        "faq1_a": "Yes! All rows and columns from your primary worksheet are converted into RFC 4180 compliant CSV format.",
        "faq2_q": "Is there a row limit?",
        "faq2_a": "No! Our engine processes tens of thousands of rows client-side in seconds."
    },
    {
        "slug": "word-to-html",
        "name": "Convert Word to HTML",
        "category": "data",
        "icon": "📝➔🌐",
        "desc": "Convert Microsoft Word (.docx) files into clean, semantically structured HTML code.",
        "keywords": "word to html online, convert docx to html, word document to web page, clean word to html",
        "input_type": "file",
        "accept": ".docx",
        "action": "/word-to-html",
        "btn_text": "Convert to HTML & Download ⚡",
        "options_html": "",
        "faq1_q": "Is the generated HTML clean?",
        "faq1_a": "Yes! It uses semantic tags (`<p>`, `<h1>`, `<h2>`, `<ul>`) rather than bloated proprietary Microsoft Word markup.",
        "faq2_q": "Can I publish the output directly online?",
        "faq2_a": "Yes! The output is a standard HTML5 document ready for web hosting or blog posting."
    },
    {
        "slug": "csv-to-json",
        "name": "Convert CSV to JSON",
        "category": "data",
        "icon": "📄➔{ }",
        "desc": "Convert tabular CSV datasets into structured JSON arrays of objects for web developers and APIs.",
        "keywords": "csv to json online, convert csv to json, tabular data to json, csv to json converter free",
        "input_type": "file",
        "accept": ".csv",
        "action": "/csv-to-json",
        "btn_text": "Convert CSV to JSON ⚡",
        "options_html": "",
        "faq1_q": "How are column headers mapped?",
        "faq1_a": "The first row in the CSV is automatically used as the keys for each JSON object in the output array.",
        "faq2_q": "Is the JSON formatted and indented?",
        "faq2_a": "Yes! The output is formatted with 2-space indentation for easy readability."
    },
    {
        "slug": "json-to-csv",
        "name": "Convert JSON to CSV",
        "category": "data",
        "icon": "{ }➔📄",
        "desc": "Convert JSON arrays of objects into Excel-ready Comma-Separated Values (.csv) spreadsheets.",
        "keywords": "json to csv online, convert json to csv, export json to excel, json to spreadsheet converter",
        "input_type": "file",
        "accept": ".json",
        "action": "/json-to-csv",
        "btn_text": "Convert JSON to CSV ⚡",
        "options_html": "",
        "faq1_q": "What JSON structures are supported?",
        "faq1_a": "Arrays of objects (e.g. `[{\"name\": \"Alice\", \"age\": 30}]`) are flattened into clean columns and rows.",
        "faq2_q": "Can I open the CSV in Excel or Google Sheets?",
        "faq2_a": "Yes! The output conforms to standard CSV formatting and opens directly in Excel, Numbers, and Sheets."
    },
    {
        "slug": "json-formatter",
        "name": "JSON Formatter & Validator",
        "category": "data",
        "icon": "{ }",
        "desc": "Validate, beautify, and format messy or minified JSON code online with instant syntax verification.",
        "keywords": "json formatter online, json validator, beautify json free, json pretty print, format json",
        "input_type": "file",
        "accept": ".json,.txt",
        "action": "/json-formatter",
        "btn_text": "Format & Beautify JSON ⚡",
        "options_html": "",
        "faq1_q": "Does this tool detect syntax errors?",
        "faq1_a": "Yes! If your JSON has missing brackets, commas, or trailing quotes, clear error details are displayed.",
        "faq2_q": "Can I format large JSON files?",
        "faq2_a": "Yes! In-browser JavaScript parses multi-megabyte JSON payloads instantly without network lag."
    },
    {
        "slug": "flip-image",
        "name": "Flip & Mirror Image",
        "category": "image",
        "icon": "↔️🖼️",
        "desc": "Flip images horizontally or vertically to mirror photos, selfies, and graphics online.",
        "keywords": "flip image online, mirror image free, flip photo horizontally, reverse photo orientation",
        "input_type": "file",
        "accept": "image/*",
        "action": "/flip-image",
        "btn_text": "Flip Image & Download ⚡",
        "options_html": """
            <div style="margin-bottom:1rem; text-align:left;">
                <label style="display:block; font-size:0.85rem; font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;">Flip Direction:</label>
                <select id="flipDir" style="width:100%; height:42px; background:#0f172a; color:#f8fafc; border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:0 0.8rem; font-weight:600;">
                    <option value="horizontal">Horizontal (Mirror Selfie)</option>
                    <option value="vertical">Vertical (Upside Down)</option>
                </select>
            </div>
        """,
        "faq1_q": "Will flipping reduce image quality?",
        "faq1_a": "No! Pixel canvas mapping preserves maximum resolution and color fidelity.",
        "faq2_q": "Can I flip front-camera mirrored selfies back to normal?",
        "faq2_a": "Yes! Select 'Horizontal' to un-mirror any inverted selfie or scanned photo."
    },
    {
        "slug": "jpg-to-png",
        "name": "Convert JPG to PNG Online",
        "category": "image",
        "icon": "JPG➔PNG",
        "desc": "Convert JPG and JPEG photos into lossless PNG format with transparency support online for free.",
        "keywords": "jpg to png online, convert jpg to png, jpeg to png converter, free jpg to png",
        "input_type": "file",
        "accept": ".jpg,.jpeg",
        "action": "/jpg-to-png",
        "btn_text": "Convert to PNG ⚡",
        "options_html": "",
        "faq1_q": "Why convert JPG to PNG?",
        "faq1_a": "PNG is a lossless format that prevents compression artifacts when editing photos or adding graphics.",
        "faq2_q": "Is the conversion instant?",
        "faq2_a": "Yes! HTML5 hardware-accelerated canvas executes the format conversion locally in milliseconds."
    },
    {
        "slug": "png-to-jpg",
        "name": "Convert PNG to JPG Online",
        "category": "image",
        "icon": "PNG➔JPG",
        "desc": "Convert PNG images into high-quality, lightweight JPG format to reduce file sizes for web uploads.",
        "keywords": "png to jpg online, convert png to jpg, png to jpeg converter free, compress png to jpg",
        "input_type": "file",
        "accept": ".png",
        "action": "/png-to-jpg",
        "btn_text": "Convert to JPG ⚡",
        "options_html": "",
        "faq1_q": "What happens to transparent backgrounds?",
        "faq1_a": "Because JPG does not support alpha transparency, transparent areas are smoothly filled with a clean white background.",
        "faq2_q": "Does this reduce file size?",
        "faq2_a": "Yes! Converting PNG screenshots and photos to JPG typically reduces file size by 60% to 80%."
    },
    {
        "slug": "webp-to-png",
        "name": "Convert WEBP to PNG Online",
        "category": "image",
        "icon": "WEBP➔PNG",
        "desc": "Convert modern Google WEBP images into universally compatible PNG format for editing and printing.",
        "keywords": "webp to png online, convert webp to png, save webp as png, webp image converter free",
        "input_type": "file",
        "accept": ".webp",
        "action": "/webp-to-png",
        "btn_text": "Convert WEBP to PNG ⚡",
        "options_html": "",
        "faq1_q": "Why do I need to convert WEBP to PNG?",
        "faq1_a": "Many older photo editing software and office applications do not support WEBP files saved from the web. PNG works everywhere.",
        "faq2_q": "Is transparency preserved from WEBP?",
        "faq2_a": "Yes! PNG supports full 32-bit RGBA transparency, preserving clean transparent backgrounds."
    },
    {
        "slug": "svg-to-png",
        "name": "Convert SVG to PNG Online",
        "category": "image",
        "icon": "SVG➔PNG",
        "desc": "Convert scalable vector SVG graphics into raster PNG images at high resolution online for free.",
        "keywords": "svg to png online, convert vector svg to png, export svg as picture, svg to png high resolution",
        "input_type": "file",
        "accept": ".svg",
        "action": "/svg-to-png",
        "btn_text": "Convert SVG to PNG ⚡",
        "options_html": "",
        "faq1_q": "Can I convert complex vector SVGs?",
        "faq1_a": "Yes! All paths, gradients, shapes, and typography in the SVG are rasterized cleanly onto a high-res PNG canvas.",
        "faq2_q": "Is transparency maintained?",
        "faq2_a": "Yes! Vector transparent canvas backgrounds remain fully transparent in the output PNG."
    },
    {
        "slug": "image-to-pdf",
        "name": "Convert Image to PDF Online",
        "category": "pdf",
        "icon": "🖼️➔📕",
        "desc": "Convert JPG, PNG, WEBP, or BMP photos into clean, print-ready PDF documents online.",
        "keywords": "image to pdf online, photo to pdf converter, convert picture to pdf, picture to pdf free",
        "input_type": "file",
        "accept": "image/*",
        "action": "/image-to-pdf",
        "btn_text": "Convert Image to PDF ⚡",
        "options_html": "",
        "faq1_q": "Can I convert photos of documents and ID cards?",
        "faq1_a": "Yes! It scales the photo to standard ISO A4 paper size and centers it for crisp printing and official submissions.",
        "faq2_q": "Does the image retain high resolution in the PDF?",
        "faq2_a": "Yes! The original pixel resolution is embedded directly into the PDF container with zero compression loss."
    }
]

print(f"Loaded {len(TOOLS_CATALOG)} tools in catalog.")
