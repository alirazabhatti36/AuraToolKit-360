"""
AuraToolKit 360 - Google AdSense Publisher Compliance Injector
Ensures all public editorial and tool pages have required AdSense tags,
Google verification, and Consent Mode v2 integration.
Excludes private/auth/admin endpoints as per AdSense policy.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUB_ID = "ca-pub-1373118680696037"
GA_ID = "G-06PT7VHV1Q"
SITE_VERIFY = "N0rLFYsip2eaN77OK361NOkyHS3eqB9i9gf2EYZkbMA"

ADSENSE_SNIPPET = f"""    <!-- Google AdSense & Search Console Verification -->
    <meta name="google-adsense-account" content="{PUB_ID}">
    <script defer src="/tracking-consent.js" data-adsense-client="{PUB_ID}" data-ga-measurement-id="{GA_ID}"></script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>
    <meta name="google-site-verification" content="{SITE_VERIFY}">
"""

# Pages that MUST NOT have AdSense (Policy violation to have ads on login/admin/checkout)
EXCLUDE_SUBSTRINGS = [
    "saas" + os.sep + "login",
    "saas" + os.sep + "subscribe",
    "saas" + os.sep + "admin",
    "saas" + os.sep + "app",
    "aura_hrm_saas",
    "widget.html",
    ".git",
    "scratch"
]

target_tools = [
    os.path.join(BASE_DIR, "cover-letter-maker", "index.html"),
    os.path.join(BASE_DIR, "converter", "word-to-pdf", "index.html"),
    os.path.join(BASE_DIR, "converter", "ocr-to-text", "index.html"),
    os.path.join(BASE_DIR, "converter", "passport-photo-maker", "index.html"),
    os.path.join(BASE_DIR, "saas", "index.html")  # SaaS marketing overview page is public
]

updated = 0
for file_path in target_tools:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if PUB_ID in content:
        print(f"Already compliant: {os.path.relpath(file_path, BASE_DIR)}")
        continue

    if "</head>" in content:
        new_content = content.replace("</head>", ADSENSE_SNIPPET + "</head>", 1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Injected AdSense tags into: {os.path.relpath(file_path, BASE_DIR)}")
        updated += 1
    else:
        print(f"No </head> in {os.path.relpath(file_path, BASE_DIR)}")

print(f"\nDone! Updated {updated} pages for AdSense compliance.")
