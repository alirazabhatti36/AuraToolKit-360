import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

candidates = [
    "index.html",
    "converter/index.html",
    "converter.html",
    "converter/word-to-pdf/index.html",
    "saas/index.html"
]

for c in candidates:
    p = os.path.join(base_dir, c.replace("/", os.sep))
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Look for Word to PDF in tags
    matches = re.finditer(r'<([^>]+)>([^<]*Word to PDF[^<]*)</\1>', content, re.IGNORECASE)
    for m in matches:
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 200)
        print(f"\n--- MATCH IN {c} ---")
        print(content[start:end])
