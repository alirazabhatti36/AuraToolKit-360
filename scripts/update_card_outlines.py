import re, os

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

converter_pages = [
    "converter/index.html",
    "converter.html",
    "templates/converter.html",
    "ar/converter/index.html",
    "de/converter/index.html",
    "es/converter/index.html",
    "fr/converter/index.html",
    "pt/converter/index.html",
    "index.html"
]

for cp in converter_pages:
    p = os.path.join(base_dir, cp.replace("/", os.sep))
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update --border-card variable
    c = c.replace("--border-card: #e2e8f0;", "--border-card: #cbd5e1;")
    c = c.replace("--border-card: rgba(255, 255, 255, 0.08);", "--border-card: #cbd5e1;")

    # 2. Update .tool-card border if present
    c = re.sub(
        r'(\.tool-card\s*\{[^}]*?)border:\s*1px\s+solid\s+#[0-9a-fA-F]+;',
        r'\1border: 1.5px solid #cbd5e1; box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -1px rgba(15, 23, 42, 0.04);',
        c
    )
    c = re.sub(
        r'(\.tool-card\s*\{[^}]*?)border:\s*1px\s+solid\s+var\(--border-card\);',
        r'\1border: 1.5px solid #cbd5e1; box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -1px rgba(15, 23, 42, 0.04);',
        c
    )

    # 3. Update .tool-icon border and background if present
    c = c.replace("border: 1px solid #e2e8f0 !important;", "border: 1.5px solid #cbd5e1 !important;")
    c = c.replace("background: #f8fafc !important;\n            border: 1px solid #e2e8f0 !important;", "background: #f1f5f9 !important;\n            border: 1.5px solid #cbd5e1 !important;")

    # 4. Update .chip-btn border if present
    c = c.replace("border: 1px solid var(--aura-border)", "border: 1.5px solid #cbd5e1")
    c = c.replace("border: 1.5px solid #cbd5e1 !important;", "border: 1.5px solid #cbd5e1 !important; box-shadow: 0 2px 5px rgba(15, 23, 42, 0.04) !important;")

    # 5. Update .pillar-card in index.html
    if "index.html" in cp:
        c = re.sub(
            r'(\.pillar-card\s*\{[^}]*?)border:\s*1px\s+solid\s+var\(--border-card\);',
            r'\1border: 1.5px solid #cbd5e1; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);',
            c
        )

    with open(p, "w", encoding="utf-8") as f:
        f.write(c)

    print(f"Updated card outlines in {cp}")

print("Completed updating card outlines across primary pages!")
