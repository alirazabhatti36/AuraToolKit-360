import os
import re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
converter_dir = os.path.join(base_dir, "converter")

existing_folders = set(os.listdir(converter_dir))

converter_index = os.path.join(converter_dir, "index.html")
with open(converter_index, "r", encoding="utf-8") as f:
    c = f.read()

cards = re.findall(r'<div class=["\']tool-card["\'][^>]*data-tool-slug=["\']([^"\']+)["\'][^>]*data-tool-name=["\']([^"\']+)["\']', c)

print(f"Cards: {len(cards)}, Existing Folders in converter/: {len(existing_folders)}")

mapped = {}
unmapped_cards = []

for slug, name in cards:
    # 1. Exact match
    if slug in existing_folders:
        mapped[slug] = slug
    # 2. Check dedicated links inside the card
    else:
        # Find the card block in HTML
        card_match = re.search(r'id=["\']tool-card-' + re.escape(slug) + r'["\'].*?</div>\s*</div>', c, re.DOTALL)
        matched_folder = None
        if card_match:
            links = re.findall(r'href=["\']/converter/([^/]+)/["\']', card_match.group(0))
            if links and links[0] in existing_folders:
                matched_folder = links[0]
            else:
                # Check root tool links
                root_links = re.findall(r'href=["\']/([^/]+)/["\']', card_match.group(0))
                for rl in root_links:
                    if os.path.isdir(os.path.join(base_dir, rl)):
                        matched_folder = "/" + rl
        
        if not matched_folder:
            # Fuzzy match folder
            clean_slug = slug.replace("-converter", "").replace("-tool", "").replace("-online", "").replace("secure-", "").replace("live-", "")
            for ef in existing_folders:
                if clean_slug in ef or ef in clean_slug:
                    matched_folder = ef
                    break

        if matched_folder:
            mapped[slug] = matched_folder
        else:
            unmapped_cards.append((slug, name))

print(f"\nMapped tools: {len(mapped)}")
for s, f in mapped.items():
    print(f"  {s} -> {f}")

print(f"\nTruly unmapped / missing dedicated pages: {len(unmapped_cards)}")
for s, n in unmapped_cards:
    print(f"  {s} ({n})")
