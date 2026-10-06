import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

print("==================================================")
print("     AURATOOLKIT 360 - COMPREHENSIVE QA AUDIT     ")
print("==================================================")

# 1. Sitemap Verification
sitemap_path = os.path.join(base_dir, "sitemap.xml")
tree = ET.parse(sitemap_path)
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [elem.text for elem in root.findall('.//ns:loc', namespace)]

sitemap_errors = []
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
    if not os.path.exists(disk_path):
        sitemap_errors.append((u, disk_path))

print(f"[TEST 1] Sitemap URLs verified: {len(urls)} | Errors: {len(sitemap_errors)}")

# 2. Internal Links & Asset Verification
html_files = []
for r, d, files in os.walk(base_dir):
    if any(ex in r for ex in [".git", "node_modules", "aura_hrm_saas", ".gemini", "scratch"]):
        continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(r, f))

broken_assets = []
broken_internal_links = []

for hp in html_files:
    rel_source = os.path.relpath(hp, base_dir).replace("\\", "/")
    source_dir = os.path.dirname(hp)
    with open(hp, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()

    # Check hrefs
    for m in re.finditer(r'href=["\']([^"\']+)["\']', c):
        href = m.group(1).strip()
        if href.startswith("http://") or href.startswith("https://") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:") or href.startswith("#") or href.startswith("data:"):
            continue
        if "${" in href:  # JS template string
            continue

        # Parse path
        path_part = urlparse(href).path
        if not path_part:
            continue

        if path_part.startswith("/"):
            target = os.path.join(base_dir, path_part.lstrip("/"))
        else:
            target = os.path.join(source_dir, path_part)

        # If directory, look for index.html
        if not os.path.exists(target):
            if os.path.exists(os.path.join(target, "index.html")):
                target = os.path.join(target, "index.html")
            elif os.path.exists(target + ".html"):
                target = target + ".html"

        if not os.path.exists(target):
            broken_internal_links.append((rel_source, href))

    # Check src (images, scripts)
    for m in re.finditer(r'src=["\']([^"\']+)["\']', c):
        src = m.group(1).strip()
        if src.startswith("http://") or src.startswith("https://") or src.startswith("data:") or src.startswith("javascript:"):
            continue
        if "${" in src:
            continue

        path_part = urlparse(src).path
        if not path_part:
            continue

        if path_part.startswith("/"):
            target = os.path.join(base_dir, path_part.lstrip("/"))
        else:
            target = os.path.join(source_dir, path_part)

        if not os.path.exists(target):
            broken_assets.append((rel_source, src))

print(f"[TEST 2] Internal links scanned across {len(html_files)} pages.")
print(f"         Broken internal links found: {len(broken_internal_links)}")
for s, l in broken_internal_links[:5]:
    print(f"           - In {s}: {l}")

print(f"[TEST 3] Local script/image assets scanned.")
print(f"         Broken local assets found: {len(broken_assets)}")
for s, a in broken_assets[:5]:
    print(f"           - In {s}: {a}")

# 4. Ad Units Check
blogs_with_ad_units = 0
blogs_total = 0
for hp in html_files:
    rel = os.path.relpath(hp, base_dir).replace("\\", "/")
    if rel.startswith("blogs/") and rel != "blogs/index.html":
        blogs_total += 1
        with open(hp, "r", encoding="utf-8") as f:
            if "atk-ad-container" in f.read():
                blogs_with_ad_units += 1

print(f"[TEST 4] Blog articles ad unit compliance: {blogs_with_ad_units} / {blogs_total} articles.")

# 5. Restricted Pages Zero Ad Check
restricted = ["saas/login/index.html", "saas/subscribe/index.html", "saas/admin/license.html", "saas/app/index.html"]
restricted_violations = 0
for rp in restricted:
    p = os.path.join(base_dir, rp.replace("/", os.sep))
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
            if "adsbygoogle" in c or "atk-ad" in c:
                restricted_violations += 1
                print(f"Violation: {rp} contains AdSense code!")

print(f"[TEST 5] Restricted pages ad-free check: {len(restricted) - restricted_violations} / {len(restricted)} clean.")

# 6. AI Filler Text Check
ai_phrases = [r"\bas an ai\b", r"\bi am an ai\b", r"\blanguage model\b", r"\blorem ipsum\b", r"\[your\s+name\]", r"\[your\s+company\]"]
ai_violations = 0
for hp in html_files:
    rel = os.path.relpath(hp, base_dir).replace("\\", "/")
    with open(hp, "r", encoding="utf-8", errors="ignore") as f:
        clean_text = re.sub(r'<[^>]+>', ' ', f.read())
        for pat in ai_phrases:
            if re.search(pat, clean_text, re.IGNORECASE):
                ai_violations += 1
                print(f"AI phrase match in: {rel}")

print(f"[TEST 6] AI filler text check: {ai_violations} violations found.")
print("==================================================")
