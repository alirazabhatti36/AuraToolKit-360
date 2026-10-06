import os, re, glob
from generate_landscape_logos import get_landscape_banner

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
dedicated_pages = glob.glob(os.path.join(base_dir, "converter", "*", "index.html"))

for dp in dedicated_pages:
    slug = os.path.basename(os.path.dirname(dp))
    with open(dp, "r", encoding="utf-8") as f:
        c = f.read()

    if "tool-hero-banner" in c:
        continue

    svg = get_landscape_banner(slug)
    banner_div = f'\n            <div class="tool-hero-banner" style="width: 180px; max-width: 100%; height: 76px; margin: 0 auto 1.4rem; background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); overflow: hidden;">{svg}</div>'

    # Insert right after <div class="...tool-card...">
    if re.search(r'<div class=["\'][^"\']*tool-card[^"\']*["\'][^>]*>', c):
        c = re.sub(r'(<div class=["\'][^"\']*tool-card[^"\']*["\'][^>]*>)', r'\1' + banner_div, c, count=1)
        with open(dp, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Injected hero banner into {slug}")
    else:
        print(f"Could not find tool-card in {slug}")

print("All dedicated tool pages now have hero banners!")
