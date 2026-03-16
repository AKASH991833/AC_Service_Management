@echo off
title Add Routes to routes.py
color 0B

echo ========================================
echo   Adding New Routes to routes.py
echo ========================================
echo.

cd /d "%~dp0backend"

echo Copying new routes...
echo.

REM Read new_routes.py and append to routes.py
type new_routes.py >> routes.py

echo.
echo ========================================
echo   Routes Added Successfully!
echo ========================================
echo.
echo Next Steps:
echo 1. Restart backend
echo 2. Open admin dashboard
echo 3. Test new features
echo.

pause
