"""
Generator for Landscape Tool SVG Banners (inspired by media_1791305285562.png)
Creates horizontal 170x68 landscape illustrations for all converter and utility tools.
"""

def get_landscape_banner(slug, title="Tool"):
    slug = slug.strip().lower()

    # Common defs for all SVGs
    defs = """
      <defs>
        <filter id="soft-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="5" result="blur" />
        </filter>
        <linearGradient id="ppt-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fb923c"/><stop offset="100%" stop-color="#ea580c"/>
        </linearGradient>
        <linearGradient id="word-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#2563eb"/>
        </linearGradient>
        <linearGradient id="excel-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#4ade80"/><stop offset="100%" stop-color="#16a34a"/>
        </linearGradient>
        <linearGradient id="pdf-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f87171"/><stop offset="100%" stop-color="#dc2626"/>
        </linearGradient>
        <linearGradient id="img-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#c084fc"/><stop offset="100%" stop-color="#7c3aed"/>
        </linearGradient>
        <linearGradient id="cyan-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#0284c7"/>
        </linearGradient>
        <linearGradient id="amber-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fcd34d"/><stop offset="100%" stop-color="#d97706"/>
        </linearGradient>
        <linearGradient id="arrow-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#818cf8"/><stop offset="100%" stop-color="#6366f1"/>
        </linearGradient>
      </defs>
    """

    # Pastel ambient backdrop like in reference image
    def clouds(c1="#fed7aa", c2="#fbcfe8", c3="#e0e7ff"):
        return f"""
        <circle cx="45" cy="34" r="24" fill="{c1}" opacity="0.45" filter="url(#soft-glow)"/>
        <circle cx="125" cy="34" r="24" fill="{c2}" opacity="0.45" filter="url(#soft-glow)"/>
        <circle cx="85" cy="34" r="20" fill="{c3}" opacity="0.5" filter="url(#soft-glow)"/>
        <circle cx="14" cy="20" r="2.2" fill="#38bdf8" opacity="0.8"/>
        <rect x="12" y="42" width="2.5" height="6" rx="1.2" transform="rotate(-30 13 45)" fill="#818cf8" opacity="0.7"/>
        <circle cx="156" cy="46" r="2.2" fill="#a855f7" opacity="0.8"/>
        <rect x="152" y="16" width="2.5" height="6" rx="1.2" transform="rotate(35 153 19)" fill="#38bdf8" opacity="0.7"/>
        """

    def center_arrow():
        return """
        <g transform="translate(74, 28)">
          <path d="M 0,6 L 13,6 L 13,2 L 22,7 L 13,12 L 13,8 L 0,8 Z" fill="url(#arrow-grad)" filter="drop-shadow(0 2px 4px rgba(99,102,241,0.3))"/>
        </g>
        """

    def pdf_card(x=106, y=10):
        return f"""
        <g transform="translate({x}, {y})">
          <path d="M 4,4 C 4,1.8 5.8,0 8,0 L 28,0 L 38,10 L 38,43 C 38,45.2 36.2,47 34,47 L 8,47 C 5.8,47 4,45.2 4,43 Z" fill="url(#pdf-grad)" filter="drop-shadow(0 4px 6px rgba(220,38,38,0.3))"/>
          <path d="M 28,0 L 28,10 L 38,10 Z" fill="#b91c1c" opacity="0.6"/>
          <path d="M 28,0 L 38,10 L 28,10 Z" fill="#ffffff" opacity="0.95"/>
          <path d="M 21,16 C 18,12 12,14 14,19 C 15,22 20,26 25,29 C 28,30 32,32 33,29 C 34,26 30,25 27,26 C 24,27 17,31 13,30 C 11,29 12,27 15,26 C 18,24 23,22 21,16 Z" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="21" y="41" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="900" font-size="8.5" letter-spacing="0.5" text-anchor="middle">PDF</text>
        </g>
        """

    def ppt_card(x=22, y=10):
        return f"""
        <g transform="translate({x}, {y})">
          <path d="M 18,4 L 32,4 L 38,10 L 38,43 C 38,45 36.5,46.5 34.5,46.5 L 18,46.5 Z" fill="#ffffff" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.12))"/>
          <path d="M 32,4 L 32,10 L 38,10 Z" fill="#cbd5e1"/>
          <path d="M 28,24 L 28,18 A 6,6 0 0,1 34,24 Z" fill="#ea580c"/>
          <path d="M 27,25 L 21,25 A 6,6 0 0,1 27,19 Z" fill="#f97316"/>
          <path d="M 27,26 L 27,32 A 6,6 0 0,1 21,26 Z" fill="#fb923c"/>
          <rect x="21" y="36" width="13" height="2" rx="1" fill="#cbd5e1"/>
          <rect x="2" y="6" width="24" height="37" rx="4" fill="url(#ppt-grad)" filter="drop-shadow(0 4px 6px rgba(234,88,12,0.3))"/>
          <rect x="2" y="6" width="6" height="37" rx="2" fill="#c2410c" opacity="0.3"/>
          <text x="14" y="31" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="800" font-size="18" text-anchor="middle">P</text>
        </g>
        """

    def word_card(x=22, y=10):
        return f"""
        <g transform="translate({x}, {y})">
          <path d="M 18,4 L 32,4 L 38,10 L 38,43 C 38,45 36.5,46.5 34.5,46.5 L 18,46.5 Z" fill="#ffffff" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.12))"/>
          <path d="M 32,4 L 32,10 L 38,10 Z" fill="#cbd5e1"/>
          <rect x="22" y="18" width="12" height="2" rx="1" fill="#93c5fd"/>
          <rect x="22" y="23" width="12" height="2" rx="1" fill="#93c5fd"/>
          <rect x="22" y="28" width="8" height="2" rx="1" fill="#93c5fd"/>
          <rect x="2" y="6" width="24" height="37" rx="4" fill="url(#word-grad)" filter="drop-shadow(0 4px 6px rgba(37,99,235,0.3))"/>
          <rect x="2" y="6" width="6" height="37" rx="2" fill="#1e40af" opacity="0.3"/>
          <text x="14" y="31" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="800" font-size="16" text-anchor="middle">W</text>
        </g>
        """

    def excel_card(x=22, y=10):
        return f"""
        <g transform="translate({x}, {y})">
          <path d="M 18,4 L 32,4 L 38,10 L 38,43 C 38,45 36.5,46.5 34.5,46.5 L 18,46.5 Z" fill="#ffffff" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.12))"/>
          <path d="M 32,4 L 32,10 L 38,10 Z" fill="#cbd5e1"/>
          <rect x="22" y="17" width="12" height="15" rx="1" fill="#dcfce7" stroke="#86efac" stroke-width="0.8"/>
          <line x1="22" y1="22" x2="34" y2="22" stroke="#86efac" stroke-width="0.8"/>
          <line x1="22" y1="27" x2="34" y2="27" stroke="#86efac" stroke-width="0.8"/>
          <line x1="28" y1="17" x2="28" y2="32" stroke="#86efac" stroke-width="0.8"/>
          <rect x="2" y="6" width="24" height="37" rx="4" fill="url(#excel-grad)" filter="drop-shadow(0 4px 6px rgba(22,163,74,0.3))"/>
          <rect x="2" y="6" width="6" height="37" rx="2" fill="#15803d" opacity="0.3"/>
          <text x="14" y="31" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="800" font-size="16" text-anchor="middle">X</text>
        </g>
        """

    def image_card(x=22, y=10, label="IMG"):
        return f"""
        <g transform="translate({x}, {y})">
          <rect x="4" y="4" width="34" height="42" rx="5" fill="url(#img-grad)" filter="drop-shadow(0 4px 6px rgba(124,58,237,0.3))"/>
          <rect x="7" y="7" width="28" height="24" rx="3" fill="#ffffff" opacity="0.95"/>
          <circle cx="14" cy="13" r="2.5" fill="#f59e0b"/>
          <path d="M 9,27 L 17,17 L 23,23 L 28,18 L 33,27 Z" fill="#8b5cf6"/>
          <text x="21" y="41" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="900" font-size="7.5" letter-spacing="0.5" text-anchor="middle">{label}</text>
        </g>
        """

    def txt_card(x=22, y=10, label="TXT"):
        return f"""
        <g transform="translate({x}, {y})">
          <rect x="4" y="4" width="34" height="42" rx="5" fill="#334155" filter="drop-shadow(0 4px 6px rgba(51,65,85,0.3))"/>
          <rect x="8" y="10" width="16" height="2" rx="1" fill="#94a3b8"/>
          <rect x="8" y="15" width="22" height="2" rx="1" fill="#cbd5e1"/>
          <rect x="8" y="20" width="20" height="2" rx="1" fill="#cbd5e1"/>
          <rect x="8" y="25" width="18" height="2" rx="1" fill="#cbd5e1"/>
          <text x="21" y="41" fill="#38bdf8" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="900" font-size="8" letter-spacing="0.5" text-anchor="middle">{label}</text>
        </g>
        """

    def csv_card(x=22, y=10):
        return f"""
        <g transform="translate({x}, {y})">
          <rect x="4" y="4" width="34" height="42" rx="5" fill="#0f766e" filter="drop-shadow(0 4px 6px rgba(15,118,110,0.3))"/>
          <rect x="8" y="9" width="26" height="18" rx="2" fill="#ffffff" opacity="0.95"/>
          <line x1="8" y1="15" x2="34" y2="15" stroke="#0f766e" stroke-width="0.8"/>
          <line x1="8" y1="21" x2="34" y2="21" stroke="#0f766e" stroke-width="0.8"/>
          <line x1="17" y1="9" x2="17" y2="27" stroke="#0f766e" stroke-width="0.8"/>
          <line x1="26" y1="9" x2="26" y2="27" stroke="#0f766e" stroke-width="0.8"/>
          <text x="21" y="41" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="900" font-size="8" letter-spacing="0.5" text-anchor="middle">CSV</text>
        </g>
        """

    def json_card(x=22, y=10):
        return f"""
        <g transform="translate({x}, {y})">
          <rect x="4" y="4" width="34" height="42" rx="5" fill="#4338ca" filter="drop-shadow(0 4px 6px rgba(67,56,202,0.3))"/>
          <text x="21" y="24" fill="#38bdf8" font-family="monospace" font-weight="800" font-size="16" text-anchor="middle">&#123; &#125;</text>
          <text x="21" y="41" fill="#ffffff" font-family="'Plus Jakarta Sans', system-ui, sans-serif" font-weight="900" font-size="7.5" letter-spacing="0.5" text-anchor="middle">JSON</text>
        </g>
        """

    # --- Match tool categories ---
    # 1. PPT to PDF
    if "ppt" in slug and "pdf" in slug:
        body = clouds("#fed7aa", "#fbcfe8") + ppt_card(22, 10) + center_arrow() + pdf_card(106, 10)

    # 2. Word to PDF
    elif ("word" in slug or "docx" in slug) and "pdf" in slug:
        body = clouds("#dbeafe", "#fbcfe8") + word_card(22, 10) + center_arrow() + pdf_card(106, 10)

    # 3. PDF to Word
    elif "pdf" in slug and ("word" in slug or "docx" in slug):
        body = clouds("#fbcfe8", "#dbeafe") + pdf_card(22, 10) + center_arrow() + word_card(106, 10)

    # 4. Excel to PDF
    elif "excel" in slug and "pdf" in slug:
        body = clouds("#dcfce7", "#fbcfe8") + excel_card(22, 10) + center_arrow() + pdf_card(106, 10)

    # 5. Image / JPG / PNG to PDF
    elif any(img_w in slug for img_w in ["jpg", "png", "jpeg", "image"]) and "pdf" in slug and not slug.startswith("pdf-to"):
        body = clouds("#f3e8ff", "#fbcfe8") + image_card(22, 10, "IMG") + center_arrow() + pdf_card(106, 10)

    # 6. PDF to Image / JPG / PNG
    elif slug.startswith("pdf-to") and any(img_w in slug for img_w in ["image", "jpg", "png"]):
        body = clouds("#fbcfe8", "#f3e8ff") + pdf_card(22, 10) + center_arrow() + image_card(106, 10, "IMG")

    # 7. Merge PDF
    elif "merge-pdf" in slug:
        body = clouds("#fee2e2", "#fbcfe8") + f"""
        <g transform="translate(24, 10)">
          <rect x="0" y="8" width="26" height="34" rx="4" fill="#f87171" opacity="0.6"/>
          <rect x="6" y="4" width="26" height="34" rx="4" fill="#ef4444" opacity="0.8"/>
          <rect x="12" y="0" width="26" height="34" rx="4" fill="url(#pdf-grad)" filter="drop-shadow(0 4px 6px rgba(220,38,38,0.3))"/>
          <text x="25" y="22" fill="#fff" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="8">PDF</text>
        </g>
        <g transform="translate(74, 28)">
          <path d="M 0,6 L 13,6 L 13,2 L 22,7 L 13,12 L 13,8 L 0,8 Z" fill="url(#arrow-grad)"/>
        </g>
        {pdf_card(106, 10)}
        <circle cx="132" cy="14" r="6" fill="#10b981"/>
        <text x="132" y="17" fill="#fff" font-family="sans-serif" font-weight="800" font-size="9" text-anchor="middle">+</text>
        """

    # 8. Split PDF
    elif "split-pdf" in slug or "delete-pages" in slug or "extract-pages" in slug:
        action_icon = "✂️" if "split" in slug or "extract" in slug else "🗑️"
        body = clouds("#fbcfe8", "#e0e7ff") + pdf_card(22, 10) + f"""
        <g transform="translate(72, 22)">
          <circle cx="12" cy="12" r="14" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>
          <text x="12" y="17" font-size="14" text-anchor="middle">{action_icon}</text>
        </g>
        <g transform="translate(108, 12)">
          <rect x="0" y="0" width="20" height="28" rx="3" fill="url(#pdf-grad)"/>
          <rect x="14" y="8" width="20" height="28" rx="3" fill="#38bdf8"/>
        </g>
        """

    # 9. Compress PDF
    elif "compress-pdf" in slug:
        body = clouds("#fee2e2", "#dbeafe") + f"""
        <g transform="translate(24, 10)">
          <rect x="0" y="0" width="34" height="46" rx="5" fill="url(#pdf-grad)" opacity="0.6"/>
          <text x="17" y="28" fill="#fff" font-family="sans-serif" font-weight="800" font-size="8" text-anchor="middle">MB</text>
        </g>
        <g transform="translate(68, 22)">
          <rect x="0" y="4" width="28" height="18" rx="4" fill="#3b82f6" opacity="0.15" stroke="#3b82f6" stroke-width="1.5"/>
          <text x="14" y="17" font-size="12" text-anchor="middle">🗜️</text>
        </g>
        <g transform="translate(112, 14)">
          <rect x="0" y="0" width="26" height="36" rx="4" fill="url(#pdf-grad)" filter="drop-shadow(0 4px 6px rgba(220,38,38,0.3))"/>
          <text x="13" y="22" fill="#fff" font-family="sans-serif" font-weight="800" font-size="7" text-anchor="middle">KB</text>
          <circle cx="26" cy="4" r="5" fill="#10b981"/>
          <text x="26" y="7" fill="#fff" font-family="sans-serif" font-weight="800" font-size="7" text-anchor="middle">✓</text>
        </g>
        """

    # 10. Lock / Unlock PDF
    elif "lock-pdf" in slug or "unlock-pdf" in slug:
        is_lock = "unlock" not in slug
        lock_emoji = "🔒" if is_lock else "🔓"
        lock_col = "#ef4444" if is_lock else "#10b981"
        body = clouds("#fee2e2", "#fef3c7") + pdf_card(40, 10) + f"""
        <g transform="translate(94, 16)">
          <circle cx="18" cy="18" r="18" fill="#ffffff" filter="drop-shadow(0 4px 10px rgba(0,0,0,0.15))"/>
          <circle cx="18" cy="18" r="14" fill="{lock_col}" opacity="0.15"/>
          <text x="18" y="24" font-size="16" text-anchor="middle">{lock_emoji}</text>
        </g>
        """

    # 11. Rotate PDF
    elif "rotate-pdf" in slug:
        body = clouds("#fee2e2", "#e0e7ff") + pdf_card(32, 10) + f"""
        <g transform="translate(90, 18)">
          <circle cx="20" cy="16" r="20" fill="#ffffff" filter="drop-shadow(0 4px 10px rgba(0,0,0,0.12))"/>
          <path d="M 28,10 A 12,12 0 1,0 32,20" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M 33,14 L 33,21 L 26,21" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="20" y="20" fill="#1e40af" font-family="sans-serif" font-weight="800" font-size="8" text-anchor="middle">90°</text>
        </g>
        """

    # 12. Add Watermark / Page Numbers
    elif "watermark" in slug or "page-number" in slug:
        badge_text = "STAMP" if "watermark" in slug else "1 2 3"
        body = clouds("#fee2e2", "#fef3c7") + pdf_card(40, 10) + f"""
        <g transform="translate(86, 20)">
          <rect x="0" y="0" width="46" height="22" rx="6" fill="#38bdf8" filter="drop-shadow(0 4px 6px rgba(56,189,248,0.3))"/>
          <text x="23" y="15" fill="#0f172a" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="8.5" text-anchor="middle">{badge_text}</text>
        </g>
        """

    # 13. CSV to JSON & JSON to CSV
    elif "csv-to-json" in slug:
        body = clouds("#ccfbf1", "#ede9fe") + csv_card(22, 10) + center_arrow() + json_card(106, 10)
    elif "json-to-csv" in slug:
        body = clouds("#ede9fe", "#ccfbf1") + json_card(22, 10) + center_arrow() + csv_card(106, 10)
    elif "excel-to-csv" in slug:
        body = clouds("#dcfce7", "#ccfbf1") + excel_card(22, 10) + center_arrow() + csv_card(106, 10)
    elif "docx-to-txt" in slug or "rtf-to-docx" in slug:
        if "rtf" in slug:
            body = clouds("#fed7aa", "#dbeafe") + txt_card(22, 10, "RTF") + center_arrow() + word_card(106, 10)
        else:
            body = clouds("#dbeafe", "#f1f5f9") + word_card(22, 10) + center_arrow() + txt_card(106, 10, "TXT")
    elif "txt-to-pdf" in slug:
        body = clouds("#f1f5f9", "#fbcfe8") + txt_card(22, 10, "TXT") + center_arrow() + pdf_card(106, 10)
    elif "pdf-to-txt" in slug:
        body = clouds("#fbcfe8", "#f1f5f9") + pdf_card(22, 10) + center_arrow() + txt_card(106, 10, "TXT")
    elif "word-to-html" in slug:
        body = clouds("#dbeafe", "#ffedd5") + word_card(22, 10) + center_arrow() + txt_card(106, 10, "HTML")

    # 14. Image Format Converters (JPG to PNG, PNG to JPG, etc.)
    elif any(x in slug for x in ["jpg-to-png", "png-to-jpg", "webp-to-png", "svg-to-png"]):
        parts = slug.split("-to-")
        left_lbl = parts[0].upper()
        right_lbl = parts[1].upper() if len(parts) > 1 else "IMG"
        body = clouds("#cffafe", "#fbcfe8") + image_card(22, 10, left_lbl) + center_arrow() + image_card(106, 10, right_lbl)

    # 15. OCR Tools
    elif "image-to-word" in slug:
        body = clouds("#f3e8ff", "#dbeafe") + image_card(22, 10, "IMG") + center_arrow() + word_card(106, 10)
    elif "image-to-excel" in slug:
        body = clouds("#f3e8ff", "#dcfce7") + image_card(22, 10, "IMG") + center_arrow() + excel_card(106, 10)
    elif "ocr" in slug:
        body = clouds("#f3e8ff", "#f1f5f9") + image_card(22, 10, "OCR") + center_arrow() + txt_card(106, 10, "TXT")

    # 15b. Photo & Signature Utilities
    elif "passport" in slug:
        body = clouds("#dbeafe", "#fbcfe8") + f"""
        <g transform="translate(28, 12)">
          <rect x="0" y="0" width="34" height="42" rx="4" fill="#0284c7"/>
          <circle cx="17" cy="16" r="6" fill="#fff"/>
          <path d="M 6,36 C 6,26 28,26 28,36 Z" fill="#fff"/>
        </g>
        {center_arrow()}
        <g transform="translate(104, 12)">
          <rect x="0" y="0" width="38" height="42" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
          <text x="19" y="18" font-size="12" text-anchor="middle">🪪</text>
          <text x="19" y="32" fill="#0284c7" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="7.5" text-anchor="middle">2×2 IN</text>
        </g>
        """
    elif "signature" in slug:
        body = clouds("#f3e8ff", "#dbeafe") + f"""
        <g transform="translate(28, 14)">
          <rect x="0" y="0" width="36" height="38" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
          <path d="M 6,24 C 12,14 16,30 22,18 C 26,26 30,22 32,24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round"/>
        </g>
        {center_arrow()}
        <g transform="translate(104, 14)">
          <rect x="0" y="0" width="38" height="38" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
          <text x="19" y="24" font-size="14" text-anchor="middle">✍️</text>
        </g>
        """
    elif "favicon" in slug:
        body = clouds("#dbeafe", "#fef3c7") + f"""
        <g transform="translate(28, 12)">
          <rect x="0" y="0" width="34" height="42" rx="5" fill="url(#img-grad)"/>
          <text x="17" y="26" font-size="16" text-anchor="middle">🎨</text>
        </g>
        {center_arrow()}
        <g transform="translate(104, 14)">
          <rect x="0" y="10" width="16" height="16" rx="3" fill="#3b82f6"/>
          <rect x="18" y="2" width="24" height="24" rx="4" fill="#10b981"/>
          <text x="30" y="18" fill="#fff" font-family="sans-serif" font-weight="900" font-size="9" text-anchor="middle">ICO</text>
        </g>
        """

    # 16. Image Editing Tools (Compress, Resize, Crop, Flip)
    elif any(x in slug for x in ["compress-image", "resize-image", "crop-rotate-image", "flip-image", "watermark-image"]):
        icon = "🗜️" if "compress" in slug else ("↔️" if "flip" in slug else ("✂️" if "crop" in slug else "📐"))
        body = clouds("#f3e8ff", "#e0e7ff") + image_card(32, 10, "IMG") + f"""
        <g transform="translate(86, 18)">
          <circle cx="20" cy="16" r="20" fill="#ffffff" filter="drop-shadow(0 4px 10px rgba(0,0,0,0.12))"/>
          <text x="20" y="22" font-size="16" text-anchor="middle">{icon}</text>
        </g>
        """

    # 16. Video & Audio
    elif "video" in slug or "mp3" in slug:
        icon_left = "🎬" if "video" in slug else "🎵"
        icon_right = "🗜️" if "compress" in slug else "🎧"
        body = clouds("#fee2e2", "#f3e8ff") + f"""
        <g transform="translate(28, 12)">
          <rect x="0" y="0" width="36" height="42" rx="6" fill="#0f172a" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.25))"/>
          <text x="18" y="27" font-size="18" text-anchor="middle">{icon_left}</text>
        </g>
        {center_arrow()}
        <g transform="translate(106, 12)">
          <rect x="0" y="0" width="36" height="42" rx="6" fill="url(#cyan-grad)" filter="drop-shadow(0 4px 6px rgba(2,132,199,0.3))"/>
          <text x="18" y="27" font-size="18" text-anchor="middle">{icon_right}</text>
        </g>
        """

    # 17. Writing Utilities (Word Counter, Case Converter, Password Generator, Paraphrasing)
    elif any(x in slug for x in ["word-count", "case-convert", "password", "paraphras"]):
        if "word-count" in slug or "counter" in slug:
            body = clouds("#dbeafe", "#e0e7ff") + f"""
            <g transform="translate(24, 10)">
              <rect x="0" y="0" width="34" height="44" rx="5" fill="#1e293b"/>
              <text x="17" y="28" font-size="16" text-anchor="middle">📝</text>
            </g>
            {center_arrow()}
            <g transform="translate(98, 12)">
              <rect x="0" y="0" width="46" height="40" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>
              <text x="23" y="18" fill="#2563eb" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="11" text-anchor="middle">1,250</text>
              <text x="23" y="32" fill="#64748b" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="7.5" text-anchor="middle">WORDS</text>
            </g>
            """
        elif "case-convert" in slug:
            body = clouds("#fbcfe8", "#dbeafe") + f"""
            <g transform="translate(28, 12)">
              <rect x="0" y="0" width="36" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
              <text x="18" y="28" fill="#64748b" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="15" text-anchor="middle">aa</text>
            </g>
            {center_arrow()}
            <g transform="translate(106, 12)">
              <rect x="0" y="0" width="36" height="42" rx="6" fill="url(#cyan-grad)"/>
              <text x="18" y="28" fill="#ffffff" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="15" text-anchor="middle">AA</text>
            </g>
            """
        elif "password" in slug:
            body = clouds("#fef3c7", "#dcfce7") + f"""
            <g transform="translate(30, 14)">
              <rect x="0" y="0" width="34" height="38" rx="6" fill="url(#amber-grad)"/>
              <text x="17" y="26" font-size="18" text-anchor="middle">🔑</text>
            </g>
            {center_arrow()}
            <g transform="translate(98, 15)">
              <rect x="0" y="0" width="48" height="36" rx="8" fill="#10b981"/>
              <text x="24" y="22" fill="#fff" font-family="monospace" font-weight="900" font-size="11" text-anchor="middle">••••••</text>
              <text x="24" y="31" fill="#ecfdf5" font-family="sans-serif" font-weight="800" font-size="6.5" text-anchor="middle">SECURE</text>
            </g>
            """
        else: # paraphrasing
            body = clouds("#f3e8ff", "#dbeafe") + f"""
            <g transform="translate(28, 12)">
              <rect x="0" y="0" width="36" height="42" rx="6" fill="#3b82f6"/>
              <text x="18" y="27" font-size="16" text-anchor="middle">✍️</text>
            </g>
            {center_arrow()}
            <g transform="translate(106, 12)">
              <rect x="0" y="0" width="36" height="42" rx="6" fill="url(#img-grad)"/>
              <text x="18" y="27" font-size="16" text-anchor="middle">✨</text>
            </g>
            """

    # 18. Everyday Calculators (Age, Time, Currency, Unit, BMI, EMI, Zakat, Percentage)
    elif any(x in slug for x in ["age", "time", "currency", "unit", "bmi", "emi", "zakat", "percent"]):
        calc_map = {
            "age": ("🎂", "📅", "DOB ➔ AGE", "#fbcfe8"),
            "time": ("⏱️", "⏳", "SEC ⇄ HRS", "#fed7aa"),
            "currency": ("💵", "💶", "LIVE FX", "#dcfce7"),
            "unit": ("📏", "📐", "METRIC ⇄ IMP", "#dbeafe"),
            "bmi": ("❤️", "⚖️", "BMI INDEX", "#fce7f3"),
            "emi": ("🏦", "📊", "LOAN EMI", "#e0e7ff"),
            "zakat": ("🌙", "🪙", "2.5% ZAKAT", "#fef3c7"),
            "percent": ("🔢", "%", "PERCENT", "#ede9fe"),
        }
        found_key = next((k for k in calc_map if k in slug), "age")
        em1, em2, badge_txt, col = calc_map[found_key]
        body = clouds(col, "#ffffff") + f"""
        <g transform="translate(24, 12)">
          <circle cx="18" cy="18" r="18" fill="#ffffff" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.1))"/>
          <text x="18" y="24" font-size="18" text-anchor="middle">{em1}</text>
        </g>
        {center_arrow()}
        <g transform="translate(94, 12)">
          <rect x="0" y="0" width="52" height="38" rx="8" fill="#1e293b" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.18))"/>
          <text x="26" y="20" font-size="13" text-anchor="middle">{em2}</text>
          <text x="26" y="32" fill="#38bdf8" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="6" text-anchor="middle">{badge_txt}</text>
        </g>
        """

    # 19. Default Fallback
    else:
        body = clouds("#e0e7ff", "#fbcfe8") + f"""
        <g transform="translate(28, 12)">
          <rect x="0" y="0" width="36" height="42" rx="6" fill="#3b82f6"/>
          <text x="18" y="27" font-size="16" text-anchor="middle">📄</text>
        </g>
        {center_arrow()}
        <g transform="translate(106, 12)">
          <rect x="0" y="0" width="36" height="42" rx="6" fill="#10b981"/>
          <text x="18" y="27" font-size="16" text-anchor="middle">⚡</text>
        </g>
        """

    return f"""<svg viewBox="0 0 170 68" width="100%" height="68" xmlns="http://www.w3.org/2000/svg" class="tool-landscape-banner" aria-hidden="true">{defs}{body}</svg>"""

if __name__ == "__main__":
    import os
    print("Testing banner generator for ppt-to-pdf:")
    svg = get_landscape_banner("ppt-to-pdf")
    print(f"Generated SVG length: {len(svg)}")
