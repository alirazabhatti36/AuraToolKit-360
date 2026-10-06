import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
converter_index = os.path.join(base_dir, "converter", "index.html")

with open(converter_index, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all tool cards
# <div class="tool-card" id="tool-card-..." data-tool-slug="..." data-tool-name="...">
cards = re.findall(r'<div class=["\']tool-card["\'][^>]*data-tool-slug=["\']([^"\']+)["\'][^>]*data-tool-name=["\']([^"\']+)["\']', content)
print(f"Total tools in converter/index.html: {len(cards)}")

existing_dirs = [d for d in os.listdir(os.path.join(base_dir, "converter")) if os.path.isdir(os.path.join(base_dir, "converter", d))]

missing_tools = []
existing_tools = []

for slug, name in cards:
    # check if folder exists in converter/
    folder = os.path.join(base_dir, "converter", slug)
    if os.path.exists(os.path.join(folder, "index.html")):
        existing_tools.append((slug, name))
    else:
        # Also check root level (like paraphrasing-tool)
        root_folder = os.path.join(base_dir, slug)
        if os.path.exists(os.path.join(root_folder, "index.html")):
            existing_tools.append((slug, name))
        else:
            missing_tools.append((slug, name))

print(f"\nAlready have dedicated page: {len(existing_tools)}")
for s, n in existing_tools:
    print(f"  [YES] {s} ({n})")

print(f"\nMissing dedicated page: {len(missing_tools)}")
for s, n in missing_tools:
    print(f"  [MISSING] {s} ({n})")
