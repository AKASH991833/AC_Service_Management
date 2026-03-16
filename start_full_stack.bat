@echo off
title Ansh Air Cool - Full Stack
color 0B

echo ========================================
echo   ANSH AIR COOL - FULL STACK STARTER
echo ========================================
echo.
echo This will start:
echo   1. Backend API Server (Port 5000)
echo   2. Frontend (Live Server)
echo.
echo Please ensure:
echo   - Python is installed
echo   - VS Code Live Server extension is installed
echo.
pause

:: Start Backend in new window
echo [1/2] Starting Backend Server...
start "Ansh Air Cool - Backend" cmd /k "%~dp0start_backend.bat"

:: Wait for backend to initialize
timeout /t 3 /nobreak >nul

:: Start Frontend with Live Server (if VS Code installed)
echo [2/2] Opening Frontend...
echo.
echo If Live Server doesn't start automatically:
echo   1. Open VS Code
echo   2. Right-click index.html
echo   3. Select "Open with Live Server"
echo.

start "" "E:\WEBISTE UI ADN BAC\frontend\index.html"

echo ========================================
echo   Servers Starting...
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: file:///E:/WEBISTE UI ADN BAC/frontend/index.html
echo.
echo Check the backend window for status
echo.
echo Press any key to exit this window...
pause >nul
