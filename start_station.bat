@echo off
title Weather Station Server
cd /d "%~dp0"
echo ========================================================
echo  Starting Poonamallee Weather Station Server...
echo  Open in browser: http://localhost:8000
echo ========================================================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
) else (
    python manage.py runserver 0.0.0.0:8000
)
pause
