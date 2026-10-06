@echo off
title AuraHR 360 - Enterprise HR, ATS & Biometrics Platform
echo ==============================================================
echo   AuraHR 360 Enterprise Platform (AuraToolKit 360)
echo   Complete HR, Biometric Attendance, Payroll & ATS System
echo ==============================================================
echo.
echo [*] Initializing backend environment...
cd /d "%~dp0aura_hrm_saas"

echo [*] Launching AuraHR Portal in default browser...
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000/login"

echo [*] Starting Python Flask server on port 5000...
echo.
python app.py
if errorlevel 1 (
    echo.
    echo [!] Server encountered an error. Press any key to exit.
    pause
)
