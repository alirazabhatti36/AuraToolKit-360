import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

target_files = [
    "converter/index.html",
    "converter.html",
    "templates/converter.html",
    "ar/converter/index.html",
    "de/converter/index.html",
    "es/converter/index.html",
    "fr/converter/index.html",
    "pt/converter/index.html"
]

NEW_CARD_CSS = """
        /* ===== ENHANCED TOOL CARD & ICON ALIGNMENT ===== */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
            gap: 1.45rem;
            align-items: stretch;
        }
        .tool-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 1.5rem 1.35rem 1.4rem;
            border: 1px solid #e2e8f0;
            transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.24s ease, border-color 0.24s ease;
            color: #0f172a;
            display: flex;
            flex-direction: column;
            position: relative;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03);
            height: 100%;
            min-height: 315px;
            box-sizing: border-box;
            overflow: hidden; /* Guarantee nothing sticks out of the card */
            font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif;
        }
        .tool-card:hover {
            transform: translateY(-4px);
            border-color: #93c5fd;
            background: #ffffff;
            box-shadow: 0 16px 32px -6px rgba(37, 99, 235, 0.12), 0 4px 12px -2px rgba(15, 23, 42, 0.04);
        }
        .tool-icon {
            display: inline-flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.45rem;
            width: fit-content;
            max-width: 100%;
            height: 42px;
            padding: 0 0.85rem;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1;
            color: #1e293b;
            white-space: nowrap !important; /* Never wrap or push emojis out of box */
            margin-bottom: 0.95rem;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
            flex-shrink: 0;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            box-sizing: border-box;
            letter-spacing: normal;
        }
        .tool-card:hover .tool-icon {
            background: #eff6ff;
            border-color: #bfdbfe;
            color: #1d4ed8;
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.1);
        }
        .tool-icon-arrow {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.82rem;
            font-weight: 800;
            color: #2563eb;
            background: rgba(37, 99, 235, 0.08);
            border: 1px solid rgba(37, 99, 235, 0.15);
            border-radius: 6px;
            width: 22px;
            height: 22px;
            line-height: 1;
            margin: 0 0.15rem;
            transition: transform 0.2s ease, background 0.2s ease;
        }
        .tool-card:hover .tool-icon-arrow {
            transform: translateX(2px);
            background: rgba(37, 99, 235, 0.18);
            border-color: rgba(37, 99, 235, 0.3);
        }
        .tool-icon-text {
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #1e293b;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .tool-card h3 {
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            font-size: 1.12rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.3;
            margin-top: 0;
            margin-bottom: 0.85rem;
            min-height: 2.75rem;
            display: flex;
            align-items: center;
            flex-shrink: 0;
            letter-spacing: -0.35px;
        }
        .tool-card label {
            display: block;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.82rem;
            color: #475569;
            font-weight: 700;
            margin-bottom: 0.45rem;
            letter-spacing: -0.1px;
        }
        .tool-card form {
            display: flex;
            flex-direction: column;
            flex: 1;
            width: 100%;
        }
        .extra-text, .tool-card .extra-text {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.82rem;
            color: #64748b;
            margin-bottom: 0.85rem;
            font-weight: 500;
            line-height: 1.5;
            flex: 1;
        }
"""

def format_icon_content(inner):
    inner = inner.strip()
    if '<span' in inner:
        # Already formatted
        return inner
    if '→' in inner:
        parts = inner.split('→', 1)
        left = parts[0].strip()
        right = parts[1].strip()
        # Check if text or emoji
        left_is_ascii = left.isalnum()
        right_is_ascii = right.isalnum()
        
        left_html = f'<span class="tool-icon-text">{left}</span>' if left_is_ascii else f'<span>{left}</span>'
        right_html = f'<span class="tool-icon-text">{right}</span>' if right_is_ascii else f'<span>{right}</span>'
        return f'{left_html}<span class="tool-icon-arrow">→</span>{right_html}'
    else:
        is_ascii = inner.isalnum()
        return f'<span class="tool-icon-text">{inner}</span>' if is_ascii else f'<span>{inner}</span>'

updated_files = 0
for rel in target_files:
    file_path = os.path.join(base_dir, rel.replace('/', os.sep))
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {rel}")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update CSS: Replace old .grid / .tool-card / .tool-icon / .tool-card h3 definitions
    # Find existing .grid / .tool-card block in style
    old_css_pattern = re.compile(
        r'\.grid\s*\{[^}]*display:\s*grid;[^}]*\}\s*'
        r'\.tool-card\s*\{[^}]*\}\s*'
        r'\.tool-card:hover\s*\{[^}]*\}\s*'
        r'\.tool-icon\s*\{[^}]*\}\s*'
        r'\.tool-card:hover\s*\.tool-icon\s*\{[^}]*\}\s*'
        r'\.tool-card\s*h3\s*\{[^}]*\}\s*'
        r'\.tool-card\s*label\s*\{[^}]*\}\s*'
        r'\.tool-card\s*form\s*\{[^}]*\}\s*'
        r'\.extra-text,\s*\.tool-card\s*\.extra-text\s*\{[^}]*\}',
        re.DOTALL
    )

    if old_css_pattern.search(content):
        content = old_css_pattern.sub(NEW_CARD_CSS.strip(), content, count=1)
        print(f"[{rel}] Successfully replaced CSS block via regex match.")
    elif "/* ===== ENHANCED TOOL CARD & ICON ALIGNMENT ===== */" not in content:
        # Fallback: Replace just before input[type="file"]
        if 'input[type="file"], input[type="text"]' in content:
            content = content.replace(
                'input[type="file"], input[type="text"]',
                NEW_CARD_CSS.strip() + '\n\n        input[type="file"], input[type="text"]',
                1
            )
            print(f"[{rel}] Injected enhanced CSS before inputs.")

    # 2. Format all <div class="tool-icon">...</div>
    def replace_tool_icon(match):
        attrs = match.group(1)
        inner = match.group(2)
        formatted = format_icon_content(inner)
        return f'<div class="tool-icon"{attrs}>{formatted}</div>'

    new_content = re.sub(r'<div class=["\']tool-icon["\']([^>]*)>(.*?)</div>', replace_tool_icon, content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[{rel}] Updated HTML and saved!")
        updated_files += 1
    else:
        # Save if CSS was modified
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{rel}] Saved CSS updates.")
        updated_files += 1

print(f"\nDone! Updated {updated_files} files.")
