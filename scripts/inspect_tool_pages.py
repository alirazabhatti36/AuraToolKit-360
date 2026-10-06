import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

tools = [
    "resume-cv-maker/index.html",
    "resume-score-checker/index.html",
    "cover-letter-maker/index.html",
    "hr-helper/index.html",
    "converter/index.html"
]

for t in tools:
    p = os.path.join(base_dir, t.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"Not found: {t}")
        continue
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    
    faq_match = "faq" in c.lower() or "guide" in c.lower() or "how it works" in c.lower() or "section" in c.lower()
    has_footer = "<footer" in c.lower()
    print(f"\nTool: {t} (length {len(c)} chars)")
    print(f"  Has FAQ/Guide: {faq_match}, Has footer: {has_footer}")
    
    # Find h2s
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', c, re.DOTALL | re.IGNORECASE)
    for h in h2s[:5]:
        clean_h = re.sub(r'<[^>]+>', '', h).strip()
        print(f"    - h2: {clean_h}")
