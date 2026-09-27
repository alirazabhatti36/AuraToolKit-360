@echo off
title AuraToolKit 360 - Enterprise HR & ATS SaaS Platform
echo ==============================================================
echo   AuraToolKit 360 - Enterprise HR & ATS SaaS Platform
echo   Local Server: http://127.0.0.1:5000/
echo ==============================================================
echo.
cd /d "%~dp0aura_hrm_saas"
start http://127.0.0.1:5000/
python app.py
pause
