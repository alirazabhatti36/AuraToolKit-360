import os, re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('tool-icon in index.html:', 'tool-icon' in c)
print('ppt-to-pdf in index.html:', 'ppt-to-pdf' in c)
print('pdf-to-word in index.html:', 'pdf-to-word' in c)

# find any tool cards or feature cards in index.html
tools_in_index = re.findall(r'<div[^>]*class=["\'][^"\']*(?:tool|converter|feature)[^"\']*["\'][^>]*>', c)
print(f'Matching divs in index.html: {len(tools_in_index)}')
for div in tools_in_index[:10]:
    print(' ', div)
