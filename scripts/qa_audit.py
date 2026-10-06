import os
import re
import sys
from urllib.parse import urlparse

# Set UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

html_files = []
for root, dirs, files in os.walk(base_dir):
    if any(ex in root for ex in [".git", "node_modules", "aura_hrm_saas", ".gemini"]):
        continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

print(f"Total HTML files to scan for QA: {len(html_files)}")

dead_hash_links = []
broken_internal_links = []
unhandled_buttons = []

# AI phrases in actual text (not HTML attributes)
ai_tell_patterns = [
    r"\bas an ai\b",
    r"\bi am an ai\b",
    r"\blanguage model\b",
    r"\blorem ipsum\b",
    r"\[insert\s+[^\]]+\]",
    r"\[your\s+name\]",
    r"\[your\s+company\]",
    r"\btodo:\s",
]
ai_matches = []

for file_path in html_files:
    rel_path = os.path.relpath(file_path, base_dir).replace("\\", "/")
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Strip script and style tags
    clean_text = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<style.*?</style>', '', clean_text, flags=re.DOTALL | re.IGNORECASE)
    # Strip HTML tags to inspect only user-visible text
    visible_text = re.sub(r'<[^>]+>', ' ', clean_text)

    for pat in ai_tell_patterns:
        for m in re.finditer(pat, visible_text, flags=re.IGNORECASE):
            start = max(0, m.start() - 30)
            end = min(len(visible_text), m.end() + 30)
            snippet = visible_text[start:end].strip().replace("\n", " ")
            ai_matches.append((rel_path, snippet))

    # 2. Check <a> links
    links = re.findall(r'<a\s+([^>]*?)>', content, re.IGNORECASE)
    for link_attrs in links:
        href_match = re.search(r'href=["\']([^"\']*)["\']', link_attrs, re.IGNORECASE)
        onclick_match = re.search(r'onclick=["\']([^"\']*)["\']', link_attrs, re.IGNORECASE)
        id_match = re.search(r'id=["\']([^"\']*)["\']', link_attrs, re.IGNORECASE)
        class_match = re.search(r'class=["\']([^"\']*)["\']', link_attrs, re.IGNORECASE)
        
        if href_match:
            href = href_match.group(1).strip()
            # If href="#" and no onclick or identifiable handler or modal trigger
            if href == "#" or href == "":
                # Exclude links that have JS handlers or known UI classes
                classes = class_match.group(1) if class_match else ""
                if not onclick_match and not id_match and not any(k in classes for k in ["btn", "modal", "trigger", "action", "tab", "toggle", "close", "menu", "chip", "nav"]):
                    dead_hash_links.append((rel_path, link_attrs))
            
            # Internal link check
            elif href.startswith("/") and not href.startswith("//"):
                parsed = urlparse(href)
                target_path = parsed.path.lstrip("/")
                if target_path == "":
                    disk_target = os.path.join(base_dir, "index.html")
                else:
                    if any(target_path.endswith(ext) for ext in [".html", ".js", ".css", ".png", ".jpg", ".jpeg", ".svg", ".xml", ".txt", ".zip", ".json", ".webp", ".ico"]):
                        disk_target = os.path.join(base_dir, target_path)
                    else:
                        disk_target = os.path.join(base_dir, target_path, "index.html")
                        if not os.path.exists(disk_target):
                            disk_target_direct = os.path.join(base_dir, target_path + ".html")
                            if os.path.exists(disk_target_direct):
                                disk_target = disk_target_direct

                if not os.path.exists(disk_target):
                    broken_internal_links.append((rel_path, href))

    # 3. Check buttons without onclick or type=submit or id or class
    buttons = re.findall(r'<button\s+([^>]*?)>', content, re.IGNORECASE)
    for b_attrs in buttons:
        has_click = 'onclick=' in b_attrs.lower()
        has_id = 'id=' in b_attrs.lower()
        has_type = 'type="submit"' in b_attrs.lower() or "type='submit'" in b_attrs.lower()
        has_class = 'class=' in b_attrs.lower()
        has_data = 'data-' in b_attrs.lower()
        if not (has_click or has_id or has_type or has_class or has_data):
            unhandled_buttons.append((rel_path, b_attrs))

print("\n--- QA REPORT RESULTS ---")
print(f"Total AI Tell Matches: {len(ai_matches)}")
for rel, snippet in ai_matches:
    print(f"  [AI Pattern in {rel}]: {snippet}")

print(f"\nDead Hash Links: {len(dead_hash_links)}")
for rel, attrs in dead_hash_links[:10]:
    print(f"  [Dead # in {rel}]: <a {attrs}>")

print(f"\nBroken Internal Links: {len(broken_internal_links)}")
# Deduplicate broken links
unique_broken = set(broken_internal_links)
for rel, href in sorted(unique_broken):
    print(f"  [Broken Link]: in {rel} -> {href}")

print(f"\nUnhandled Buttons: {len(unhandled_buttons)}")
for rel, b_attrs in unhandled_buttons[:10]:
    print(f"  [Unhandled Button in {rel}]: <button {b_attrs}>")
