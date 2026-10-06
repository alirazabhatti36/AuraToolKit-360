import os
import glob
import re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

MID_AD_SNIPPET = """
            <!-- AuraToolkit360 - Compliant AdSense In-Article Unit -->
            <div class="atk-ad-container" style="margin: 2.75rem auto; text-align: center; max-width: 100%; clear: both; overflow: hidden; padding: 0.5rem 0;">
                <div style="font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted, #64748b); margin-bottom: 0.4rem; font-weight: 600;">Advertisement</div>
                <ins class="adsbygoogle"
                     style="display:block; text-align:center;"
                     data-ad-layout="in-article"
                     data-ad-format="fluid"
                     data-ad-client="ca-pub-1373118680696037"
                     data-ad-slot="auto"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({});
                </script>
            </div>
"""

BOTTOM_AD_SNIPPET = """
            <!-- AuraToolkit360 - Compliant AdSense Article Footer Unit -->
            <div class="atk-ad-container" style="margin: 2.75rem auto; text-align: center; max-width: 100%; clear: both; overflow: hidden; padding: 0.5rem 0;">
                <div style="font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted, #64748b); margin-bottom: 0.4rem; font-weight: 600;">Advertisement</div>
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-1373118680696037"
                     data-ad-slot="auto"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({});
                </script>
            </div>
"""

# 1. Update all 35 blog articles
blog_dirs = glob.glob(os.path.join(base_dir, "blogs", "*"))
blogs_updated = 0

for b_dir in blog_dirs:
    idx_path = os.path.join(b_dir, "index.html")
    if not os.path.isfile(idx_path) or os.path.basename(b_dir) == "index.html":
        continue

    with open(idx_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if ads already inserted
    if "atk-ad-container" in content:
        continue

    modified = False

    # Placement 1: Mid-article (after 2nd <h2> section)
    h2_matches = list(re.finditer(r'<h2[^>]*>', content, re.IGNORECASE))
    if len(h2_matches) >= 3:
        # Place before the 3rd <h2> (so it sits right after the 2nd section)
        pos = h2_matches[2].start()
        content = content[:pos] + MID_AD_SNIPPET + "\n" + content[pos:]
        modified = True
    elif len(h2_matches) >= 2:
        pos = h2_matches[1].start()
        content = content[:pos] + MID_AD_SNIPPET + "\n" + content[pos:]
        modified = True

    # Placement 2: Bottom-article (before author-box or FAQ or social share)
    if '<div class="author-box">' in content:
        content = content.replace('<div class="author-box">', BOTTOM_AD_SNIPPET + '\n            <div class="author-box">', 1)
        modified = True
    elif '<h2>Frequently Asked Questions' in content:
        content = content.replace('<h2>Frequently Asked Questions', BOTTOM_AD_SNIPPET + '\n            <h2>Frequently Asked Questions', 1)
        modified = True

    if modified:
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(content)
        blogs_updated += 1

print(f"Updated {blogs_updated} blog articles with policy-compliant ad units.")

# 2. Update blogs/index.html
blogs_index = os.path.join(base_dir, "blogs", "index.html")
if os.path.exists(blogs_index):
    with open(blogs_index, "r", encoding="utf-8") as f:
        bi_content = f.read()
    
    if "atk-ad-container" not in bi_content and 'id="featuredPost"' in bi_content:
        # Insert after featuredPost
        pattern = r'(</div>\s*<!--\s*All Blog Cards Grid\s*-->)'
        match = re.search(pattern, bi_content)
        if match:
            banner_ad = """
        <!-- AuraToolkit360 - Compliant AdSense Directory Banner Unit -->
        <div class="atk-ad-container" style="margin: 2rem auto 3rem; text-align: center; max-width: 100%; clear: both; overflow: hidden; padding: 0.5rem 0;">
            <div style="font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted, #64748b); margin-bottom: 0.4rem; font-weight: 600;">Advertisement</div>
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-1373118680696037"
                 data-ad-slot="auto"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
        </div>
"""
            bi_content = bi_content[:match.start()] + banner_ad + "\n" + bi_content[match.start():]
            with open(blogs_index, "w", encoding="utf-8") as f:
                f.write(bi_content)
            print("Updated blogs/index.html with directory banner ad unit.")

