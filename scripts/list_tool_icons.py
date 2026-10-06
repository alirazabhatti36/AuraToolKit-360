import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

p = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360\converter\index.html"
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

icons = re.findall(r'<div class=["\']tool-icon["\']>(.*?)</div>', c)
print(f"Total tool-icons found in converter/index.html: {len(icons)}")
for icon in sorted(set(icons)):
    print(" ", repr(icon))

# Also check other files like converter.html, localized converter pages
files_to_check = [
    "converter.html",
    "ar/converter/index.html",
    "de/converter/index.html",
    "es/converter/index.html",
    "fr/converter/index.html",
    "pt/converter/index.html",
    "templates/converter.html"
]

for fc in files_to_check:
    import os
    full = os.path.join(r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360", fc.replace("/", os.sep))
    if os.path.exists(full):
        with open(full, "r", encoding="utf-8") as f:
            cf = f.read()
        icons_f = re.findall(r'<div class=["\']tool-icon["\']>(.*?)</div>', cf)
        print(f"File {fc}: {len(icons_f)} tool-icons")
