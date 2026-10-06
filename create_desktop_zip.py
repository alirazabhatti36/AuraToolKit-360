import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "saas", "downloads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
ZIP_PATH = os.path.join(OUTPUT_DIR, "AuraHR_Desktop_Setup.zip")
ROOT_ZIP_PATH = os.path.join(BASE_DIR, "AuraHR_Desktop_Setup.zip")

readme_content = """========================================================================
⚡ AuraHR Enterprise Desktop — Quick Installation & Setup Guide ⚡
========================================================================

Welcome to AuraHR Enterprise!
This on-premise desktop edition runs 100% locally on your computer / server.
All employee records, payroll, biometric attendance logs, and databases 
stay secure on your machine with zero cloud latency.

------------------------------------------------------------------------
HOW TO START (Takes 10 Seconds):
------------------------------------------------------------------------
1. Extract all files from this ZIP package into any folder (e.g. C:\\AuraHR).
2. Double-click "AuraHR_Desktop.bat" or "AuraHR_Desktop.vbs".
3. AuraHR will automatically start in a dedicated Desktop App window!

------------------------------------------------------------------------
DEFAULT LOGIN CREDENTIALS:
------------------------------------------------------------------------
* Super Admin Login:
    Username: superadmin
    Password: admin123

* Company Admin Login:
    Username: admin
    Password: admin123

* HR Manager Login:
    Username: hr_manager
    Password: admin123

------------------------------------------------------------------------
SUBSCRIPTION & LICENSE:
------------------------------------------------------------------------
* A 14-day Free Trial is enabled automatically upon initial launch.
* To activate your permanent license key, open the app, click "License"
  in the top bar, paste your activation key, and click "Activate".

Official Support & License Renewal: https://auratoolkit360.com
WhatsApp Helpline: +92 300 0000000
========================================================================
"""

readme_path = os.path.join(BASE_DIR, "HOW_TO_INSTALL.txt")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"Creating standalone distribution zip at: {ZIP_PATH} ...")

exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.idea', '.vscode'}
exclude_exts = {'.pyc', '.tmp', '.log'}

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Root launchers and docs
    zipf.write(readme_path, "HOW_TO_INSTALL.txt")
    
    desktop_bat = os.path.join(BASE_DIR, "AuraHR_Desktop.bat")
    if os.path.exists(desktop_bat):
        zipf.write(desktop_bat, "AuraHR_Desktop.bat")

    desktop_vbs = os.path.join(BASE_DIR, "AuraHR_Desktop.vbs")
    if os.path.exists(desktop_vbs):
        zipf.write(desktop_vbs, "AuraHR_Desktop.vbs")

    start_bat = os.path.join(BASE_DIR, "start_aurahr.bat")
    if os.path.exists(start_bat):
        zipf.write(start_bat, "start_aurahr.bat")

    # 2. Add aura_hrm_saas directory
    saas_dir = os.path.join(BASE_DIR, "aura_hrm_saas")
    for root, dirs, files in os.walk(saas_dir):
        # Exclude pycache and hidden dirs
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in exclude_exts):
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, BASE_DIR)
            zipf.write(abs_path, rel_path)

# Also copy to root for quick access
import shutil
shutil.copy2(ZIP_PATH, ROOT_ZIP_PATH)

print(f"[OK] Successfully created {ZIP_PATH} ({os.path.getsize(ZIP_PATH) / (1024*1024):.2f} MB)")
print(f"[OK] Also copied to {ROOT_ZIP_PATH}")
