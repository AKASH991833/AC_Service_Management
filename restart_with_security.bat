@echo off
title Security Update - Backend Restart
color 0A

echo ========================================
echo   ANSH AIR COOL - SECURITY UPDATE
echo   Backend Restart with Enhanced Security
echo ========================================
echo.
echo Stopping current backend process...
echo (Press Ctrl+C in the other window if still running)
echo.

REM Kill any existing Python processes running main.py
taskkill /F /FI "WINDOWTITLE eq Ansh Air Cool*" /FI "IMAGENAME eq python.exe" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting backend with ENHANCED SECURITY...
echo.
echo Security Features Enabled:
echo   [✓] Enhanced Authentication
echo   [✓] Rate Limiting (100/day, 20/hour)
echo   [✓] Input Validation & Sanitization
echo   [✓] Security Headers (XSS, Clickjacking protection)
echo   [✓] CORS Protection (localhost only)
echo   [✓] Session Security (1 hour timeout)
echo   [✓] Audit Logging
echo   [✓] File Upload Security (5MB max)
echo   [✓] SQL Injection Prevention
echo.
echo Backend will run on: http://localhost:5000
echo Admin Dashboard: frontend/admin/index.html
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

cd /d "%~dp0backend"
python main.py

pause
