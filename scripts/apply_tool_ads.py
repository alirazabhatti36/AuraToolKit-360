import os
import re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

TOOL_AD_SNIPPET = """
    <!-- AuraToolkit360 - Compliant AdSense Educational Guide Unit -->
    <div class="atk-ad-container" style="margin: 3rem auto; text-align: center; max-width: 1100px; clear: both; overflow: hidden; padding: 1rem 0;">
        <div style="font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; margin-bottom: 0.5rem; font-weight: 600;">Advertisement</div>
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

tools = [
    "resume-cv-maker/index.html",
    "resume-score-checker/index.html",
    "cover-letter-maker/index.html",
    "hr-helper/index.html",
    "converter/index.html"
]

updated_count = 0
for t in tools:
    p = os.path.join(base_dir, t.replace("/", os.sep))
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    
    if "atk-ad-container" in c:
        print(f"Already has ad container: {t}")
        continue
    
    # Target FAQ section
    faq_target = re.search(r'(<h2[^>]*>.*?Frequently Asked Questions.*?</h2>)', c, re.IGNORECASE)
    if faq_target:
        pos = faq_target.start()
        new_c = c[:pos] + TOOL_AD_SNIPPET + "\n    " + c[pos:]
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_c)
        print(f"Injected compliant ad unit into: {t}")
        updated_count += 1
    else:
        print(f"Could not find FAQ target in: {t}")

print(f"\nDone! Updated {updated_count} primary tool pages.")
