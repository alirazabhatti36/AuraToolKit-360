import os
import zipfile
import shutil

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
source_dir = os.path.join(base_dir, "aura_hrm_saas")
output_dir = os.path.join(base_dir, "assets", "downloads")
os.makedirs(output_dir, exist_ok=True)
zip_path = os.path.join(output_dir, "AuraHR_Desktop_Setup.zip")

BAT_CONTENT = """@echo off
title AuraHR 360 Enterprise - Local Desktop App
color 0b
echo =====================================================================
echo           AURA HR 360 ENTERPRISE - DESKTOP LOCAL SYSTEM
echo =====================================================================
echo.
echo Checking Python runtime environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Be sure to check 'Add Python to PATH' during installation.
    echo.
    pause
    exit /b 1
)

echo [1/2] Verifying dependencies...
pip install -r requirements.txt --quiet

echo [2/2] Launching dedicated Desktop Window...
python desktop_launcher.py

echo.
echo AuraHR Enterprise closed.
pause
"""

README_CONTENT = """=====================================================================
          AURA HR 360 ENTERPRISE - DESKTOP APPLICATION GUIDE
=====================================================================

Thank you for choosing AuraHR 360 Enterprise.
Your entire HR, payroll, attendance, and employee system runs 100% locally
on your machine for maximum confidentiality, speed, and zero server downtime.

GETTING STARTED:
1. Double-click "Launch_AuraHR_Enterprise.bat" to start the app.
2. The application will open in a dedicated, high-speed standalone desktop window.

LICENSE ACTIVATION:
- To activate your subscription or license key, visit:
  https://auratoolkit360.com/saas/subscribe/
- Choose your plan (Monthly, Annual, or Lifetime Enterprise).
- Enter the generated License Key into the AuraHR Desktop settings to unlock
  unlimited employee records, Hikvision biometric sync, and payroll exports.

SUPPORT & DOCUMENTATION:
- Official Portal: https://auratoolkit360.com/saas/
- Support: support@auratoolkit360.com

Copyright (c) 2026 AuraToolkit360. All rights reserved.
"""

# Files & folders to include
INCLUDE_ITEMS = [
    "app.py",
    "desktop_launcher.py",
    "requirements.txt",
    "firebase_config.py",
    "license_manager.py",
    "license_generator.py",
    "hikvision_bridge.py",
    "modules",
    "static",
    "templates",
    "databases"
]

print(f"Creating zip file at: {zip_path}")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    # Add BAT file
    zipf.writestr("Launch_AuraHR_Enterprise.bat", BAT_CONTENT)
    # Add README
    zipf.writestr("INSTALLATION_GUIDE.txt", README_CONTENT)
    
    # Add app files
    for item in INCLUDE_ITEMS:
        item_path = os.path.join(source_dir, item)
        if not os.path.exists(item_path):
            print(f"Warning: Item {item} not found in {source_dir}")
            continue
        
        if os.path.isfile(item_path):
            zipf.write(item_path, arcname=os.path.join("aura_hrm", item))
        elif os.path.isdir(item_path):
            for root, dirs, files in os.walk(item_path):
                # Skip cache and scratch
                if any(x in root for x in ["__pycache__", ".git", "scratch"]):
                    continue
                for file in files:
                    if file.endswith(".pyc") or file.endswith(".tmp"):
                        continue
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, source_dir)
                    zipf.write(full_p, arcname=os.path.join("aura_hrm", rel_p))

size_mb = os.path.getsize(zip_path) / (1024 * 1024)
print(f"Success! {zip_path} created. Size: {size_mb:.2f} MB")
