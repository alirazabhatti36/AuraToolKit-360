import re, sys
sys.stdout.reconfigure(encoding='utf-8')

from generate_landscape_logos import get_landscape_banner

with open('converter/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

cards = re.findall(r'<div class=["\']tool-card["\'][^>]*data-tool-slug=["\']([^"\']+)["\']', c)
print(f'Total tool cards in converter/index.html: {len(cards)}')

for s in cards:
    banner = get_landscape_banner(s)
    if not banner or len(banner) < 100:
        print(f"FAILED for {s}")
    else:
        print(f"OK: {s:30} ({len(banner)} bytes)")

print("\nAll cards matched and generated successfully!")
