import glob, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

tools = glob.glob('converter/*/index.html')
print(f'Total dedicated tool pages: {len(tools)}')

with_tool_icon = []
without_tool_icon = []

for t in tools:
    with open(t, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    m = re.findall(r'<div class=["\']tool-icon["\'][^>]*>(.*?)</div>', c)
    if m:
        with_tool_icon.append((t, m[0].strip()))
    else:
        # check for other icon markup
        m2 = re.findall(r'<div class=["\'](?:icon|hero-icon|tool-hero-icon)["\'][^>]*>(.*?)</div>', c)
        without_tool_icon.append((t, m2[0].strip() if m2 else 'NONE'))

print(f"Has tool-icon: {len(with_tool_icon)}")
print(f"Does NOT have tool-icon: {len(without_tool_icon)}")

print("\nSample with tool-icon:")
for t, icon in with_tool_icon[:10]:
    print(f"  {t}: {repr(icon)}")

print("\nSample without tool-icon:")
for t, icon in without_tool_icon[:10]:
    print(f"  {t}: {repr(icon)}")
