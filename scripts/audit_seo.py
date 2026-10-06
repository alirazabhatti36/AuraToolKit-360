import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
sitemap_path = os.path.join(base_dir, "sitemap.xml")

tree = ET.parse(sitemap_path)
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

urls = [elem.text for elem in root.findall('.//ns:loc', namespace)]

missing_title = []
missing_desc = []
missing_canonical = []
missing_viewport = []

for u in urls:
    rel = u.replace("https://auratoolkit360.com/", "")
    if rel == "":
        disk_path = os.path.join(base_dir, "index.html")
    else:
        disk_path = os.path.join(base_dir, rel.rstrip("/"), "index.html")
        if not os.path.exists(disk_path):
            disk_path2 = os.path.join(base_dir, rel)
            if os.path.exists(disk_path2):
                disk_path = disk_path2

    with open(disk_path, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()

    if "<title>" not in c.lower():
        missing_title.append(rel)
    if 'name="description"' not in c.lower() and "name='description'" not in c.lower():
        missing_desc.append(rel)
    if 'rel="canonical"' not in c.lower() and "rel='canonical'" not in c.lower():
        missing_canonical.append(rel)
    if 'name="viewport"' not in c.lower() and "name='viewport'" not in c.lower():
        missing_viewport.append(rel)

print(f"Total checked sitemap pages: {len(urls)}")
print(f"Missing <title>: {len(missing_title)}")
print(f"Missing description: {len(missing_desc)}")
for m in missing_desc:
    print("  No description:", m)
print(f"Missing canonical: {len(missing_canonical)}")
for m in missing_canonical:
    print("  No canonical:", m)
print(f"Missing viewport: {len(missing_viewport)}")
