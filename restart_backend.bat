@echo off
title Restart Backend - CORS Fix
color 0A

echo ========================================
echo   ANSH AIR COOL - BACKEND RESTART
echo   CORS Fix Applied
echo ========================================
echo.
echo Stopping current backend process...
echo (Press Ctrl+C in the other window if still running)
echo.
pause

echo.
echo Starting backend with CORS fixes...
echo.

cd /d "%~dp0"

REM Kill any existing Python processes running main.py
taskkill /F /FI "WINDOWTITLE eq Ansh Air Cool*" /FI "IMAGENAME eq python.exe" 2>nul
timeout /t 2 /nobreak >nul

echo Backend starting on: http://localhost:5000
echo Admin Dashboard: frontend/admin/index.html
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python main.py

pause
