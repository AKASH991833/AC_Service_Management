@echo off
echo ========================================
echo RESTARTING BACKEND SERVER...
echo ========================================
echo.

:: Kill any running Python processes
echo Stopping existing backend...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

:: Start new backend server
echo Starting new backend server...
cd /d "%~dp0backend"
start "Python Backend Server" python main.py

echo.
echo ========================================
echo BACKEND RESTARTED!
echo ========================================
echo.
echo Server is starting on: http://localhost:5000
echo.
echo Test health endpoint:
echo http://localhost:5000/health
echo.
echo Press any key to exit this window...
pause >nul
