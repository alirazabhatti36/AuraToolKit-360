import re, sys
sys.stdout.reconfigure(encoding='utf-8')

slugs = ['ppt-to-pdf', 'word-to-pdf', 'compress-pdf', 'merge-pdf', 'rotate-pdf']
for s in slugs:
    p = f'converter/{s}/index.html'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'(<div class=["\']tool-card["\'][^>]*>.*?)(?:<form|<input|<button)', c, re.DOTALL)
    print(f'=== {s} ===')
    if m:
        print(m.group(1).strip()[:300])
