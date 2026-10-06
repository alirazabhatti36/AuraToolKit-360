import os, re, glob
from generate_landscape_logos import get_landscape_banner

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

# 1. Update converter suite pages (converter/index.html, converter.html, templates/converter.html, localized)
converter_pages = [
    "converter/index.html",
    "converter.html",
    "templates/converter.html",
    "ar/converter/index.html",
    "de/converter/index.html",
    "es/converter/index.html",
    "fr/converter/index.html",
    "pt/converter/index.html"
]

banner_css = """
        .tool-icon {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            max-width: 100% !important;
            height: 74px !important;
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 14px !important;
            margin-bottom: 0.95rem !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
            flex-shrink: 0 !important;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            padding: 2px !important;
        }
        .tool-card:hover .tool-icon {
            background: #eff6ff !important;
            border-color: #bfdbfe !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 14px rgba(37, 99, 235, 0.1) !important;
        }
        .tool-landscape-banner {
            width: 100% !important;
            height: 100% !important;
            max-height: 70px !important;
            display: block !important;
        }
"""

def update_converter_page(rel_path):
    p = os.path.join(base_dir, rel_path.replace("/", os.sep))
    if not os.path.exists(p):
        return
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()

    # Ensure CSS contains our landscape tool-icon rules
    if ".tool-landscape-banner" not in c:
        # replace .tool-icon CSS or insert before </style>
        if ".tool-icon {" in c:
            # Replace existing .tool-icon rules
            c = re.sub(r'\.tool-icon\s*\{[^}]*\}(?:\s*\.tool-card:hover\s*\.tool-icon\s*\{[^}]*\})?', banner_css.strip(), c, count=1)
        else:
            c = c.replace("</style>", banner_css + "\n    </style>", 1)

    # Find each tool card and update its <div class="tool-icon">...</div> with the SVG banner
    def replace_card_icon(match):
        full_card_start = match.group(1)
        slug = match.group(2)
        # Generate banner
        svg = get_landscape_banner(slug)
        return f'{full_card_start}<div class="tool-icon">{svg}</div>'

    # Match <div class="tool-card"[^>]*data-tool-slug="([^"]+)"[^>]*><div class="tool-icon">.*?</div>
    pattern = r'(<div class=["\']tool-card["\'][^>]*data-tool-slug=["\']([^"\']+)["\'][^>]*>)\s*<div class=["\']tool-icon["\'][^>]*>.*?</div>'
    new_c, count = re.subn(pattern, replace_card_icon, c, flags=re.DOTALL)

    if count > 0:
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_c)
        print(f"Updated {rel_path}: replaced {count} card icons with landscape SVG banners.")
    else:
        print(f"No card icons matched in {rel_path}")

for cp in converter_pages:
    update_converter_page(cp)

# 2. Update dedicated tool pages under converter/*/index.html
dedicated_pages = glob.glob(os.path.join(base_dir, "converter", "*", "index.html"))
print(f"\nProcessing {len(dedicated_pages)} dedicated tool pages...")

for dp in dedicated_pages:
    slug = os.path.basename(os.path.dirname(dp))
    with open(dp, "r", encoding="utf-8") as f:
        c = f.read()

    svg = get_landscape_banner(slug)
    banner_div = f'<div class="tool-hero-banner" style="width: 180px; max-width: 100%; height: 76px; margin: 0 auto 1rem; background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); overflow: hidden;">{svg}</div>'

    modified = False

    # Check if there is <div class="tool-icon" ...>...</div>
    if re.search(r'<div class=["\']tool-icon["\'][^>]*>.*?</div>', c, re.DOTALL):
        c = re.sub(r'<div class=["\']tool-icon["\'][^>]*>.*?</div>', banner_div, c, count=1, flags=re.DOTALL)
        modified = True

    # Check if there is <div class="file-upload-box"[^>]*>\s*<div class="icon">.*?</div>
    elif re.search(r'(<div class=["\']file-upload-box["\'][^>]*>\s*)<div class=["\']icon["\'][^>]*>.*?</div>', c, re.DOTALL):
        c = re.sub(r'(<div class=["\']file-upload-box["\'][^>]*>\s*)<div class=["\']icon["\'][^>]*>.*?</div>', r'\1' + banner_div, c, count=1, flags=re.DOTALL)
        modified = True

    if modified:
        with open(dp, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Updated dedicated tool page: {slug}")
    else:
        print(f"Skipped (no icon pattern found): {slug}")

print("\nDone applying landscape banners across all pages!")
