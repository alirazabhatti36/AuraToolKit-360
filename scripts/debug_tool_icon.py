import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

p = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360\converter\index.html"
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

# Find all CSS rules containing tool-icon or tool-card
style_match = re.search(r'<style[^>]*>(.*?)</style>', c, re.DOTALL)
if style_match:
    style_text = style_match.group(1)
    for rule in re.findall(r'([^{}]+{[^{}]+})', style_text):
        if 'tool-icon' in rule or 'tool-card' in rule:
            print(rule.strip())
            print("-" * 40)
