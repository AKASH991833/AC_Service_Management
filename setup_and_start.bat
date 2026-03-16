@echo off
title Ansh Air Cool - Complete Setup
color 0B

echo ========================================
echo   ANSH AIR COOL - COMPLETE SETUP
echo ========================================
echo.
echo This script will:
echo   1. Check Python installation
echo   2. Install backend dependencies
echo   3. Setup database
echo   4. Start backend server
echo   5. Open frontend in browser
echo.
echo Please wait...
echo ========================================
echo.

:: Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)
echo OK: Python found
echo.

:: Navigate to backend directory
cd /d "%~dp0backend"

:: Check if virtual environment exists
if not exist "venv" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    echo OK: Virtual environment created
) else (
    echo OK: Virtual environment already exists
)
echo.

:: Activate virtual environment and install dependencies
echo [3/5] Installing backend dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
echo OK: Dependencies installed
echo.

:: Initialize database if needed
if not exist "instance" (
    echo [4/5] Creating database...
    mkdir instance
    python init_db.py
    echo OK: Database created
) else (
    echo OK: Database already exists
)
echo.

:: Deactivate virtual environment
deactivate

:: Go back to root directory
cd /d "%~dp0"

:: Start backend in new window
echo [5/5] Starting services...
echo.
start "Ansh Air Cool - Backend" cmd /k "cd backend && venv\Scripts\activate && python main.py"

:: Wait for backend to start
echo Waiting for backend to start (5 seconds)...
timeout /t 5 /nobreak >nul

:: Open frontend
echo.
echo Opening frontend in your default browser...
start "" "%~dp0frontend\index.html"

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: file:///%~dp0frontend\index.html
echo.
echo The backend server is running in a separate window.
echo Do not close that window while using the website.
echo.
echo To stop the backend:
echo   1. Go to the backend window
echo   2. Press Ctrl+C
echo.
echo ========================================
echo.
pause
