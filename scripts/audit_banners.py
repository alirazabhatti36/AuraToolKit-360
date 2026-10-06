import re

files_to_check = [
    'converter/index.html',
    'converter.html',
    'templates/converter.html',
    'ar/converter/index.html',
    'de/converter/index.html',
    'es/converter/index.html',
    'fr/converter/index.html',
    'pt/converter/index.html'
]

for f in files_to_check:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    banners = len(re.findall(r'tool-landscape-banner', c))
    cards = len(re.findall(r'class="tool-card"', c))
    print(f"{f:28}: {cards} cards | {banners} landscape banners")
