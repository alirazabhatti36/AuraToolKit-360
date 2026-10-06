import os
import re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

html_files = []
for root, dirs, files in os.walk(base_dir):
    if any(excluded in root for excluded in [".git", "node_modules", "aura_hrm_saas", ".gemini"]):
        continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

print(f"Total HTML files found: {len(html_files)}")

adsense_in_head = []
ads_units_found = []
missing_adsense = []
blogs = []
tools = []
others = []

for p in html_files:
    rel = os.path.relpath(p, base_dir).replace("\\", "/")
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    
    if "ca-pub-1373118680696037" in c:
        adsense_in_head.append(rel)
    else:
        missing_adsense.append(rel)
        
    if "adsbygoogle" in c:
        ads_units_found.append(rel)
        
    if rel.startswith("blogs/"):
        blogs.append(rel)
    elif rel.startswith("converter/") or "maker" in rel or "checker" in rel or "compressor" in rel:
        tools.append(rel)
    else:
        others.append(rel)

print(f"AdSense tag present in head: {len(adsense_in_head)}")
print(f"Missing AdSense tag in head: {len(missing_adsense)}")
print(f"Pages with adsbygoogle element: {len(ads_units_found)}")
print(f"Blogs count: {len(blogs)}")
print(f"Tools count: {len(tools)}")
print(f"Others count: {len(others)}")

print("\nMissing AdSense in head:")
for m in missing_adsense:
    print(" -", m)

print("\nPages that currently have adsbygoogle unit:")
for a in ads_units_found:
    print(" -", a)
