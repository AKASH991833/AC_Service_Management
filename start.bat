@echo off
chcp 65001 >nul
echo ========================================
echo   ANSH AIR COOL - QUICK START
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

:: Navigate to backend directory
cd /d "%~dp0backend"

:: Install dependencies
echo [2/4] Installing Python dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

:: Initialize database
echo [3/4] Initializing database...
python init_db.py
if errorlevel 1 (
    echo [ERROR] Database initialization failed
    echo Check MySQL connection and credentials
    pause
    exit /b 1
)
echo.

:: Start backend server
echo [4/4] Starting backend server...
echo.
echo ========================================
echo   BACKEND IS RUNNING!
echo   API: http://localhost:5000
echo   Health: http://localhost:5000/health
echo ========================================
echo.
echo NEXT STEP:
echo 1. Open frontend folder in VS Code
echo 2. Right-click index.html
echo 3. Select "Open with Live Server"
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python main.py
