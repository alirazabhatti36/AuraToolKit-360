import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for f in ["index.html", "converter/index.html"]:
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    print(f"=== {f} ===")
    print("tool-card in file:", "tool-card" in c)
    print("tool-icon in file:", "tool-icon" in c)
    print("Word to PDF in file:", "Word to PDF" in c)
    if "Word to PDF" in c:
        for m in re.finditer(r'Word to PDF', c):
            start = max(0, m.start() - 100)
            end = min(len(c), m.end() + 100)
            print("  Context:", repr(c[start:end]))
