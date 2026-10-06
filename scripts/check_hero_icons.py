import glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob('converter/*/index.html')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    # Find any tool-icon or icon in hero
    m = re.findall(r'<div class=["\'][^"\']*icon[^"\']*["\'][^>]*>(.*?)</div>', c)
    slug = f.replace('\\', '/').split('/')[1]
    val = m[0].strip() if m else "NONE"
    print(f'{slug:25}: {repr(val)[:60]}')
