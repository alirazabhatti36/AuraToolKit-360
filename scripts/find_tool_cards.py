import os

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
matched_files = []

for root, dirs, files in os.walk(base_dir):
    if any(ex in root for ex in [".git", "node_modules", "aura_hrm_saas", ".gemini"]):
        continue
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                c = fp.read()
            if "tool-card" in c or "tool-icon" in c:
                matched_files.append(os.path.relpath(p, base_dir).replace("\\", "/"))

print(f"Total files with tool-card or tool-icon: {len(matched_files)}")
for mf in matched_files:
    print(" -", mf)
