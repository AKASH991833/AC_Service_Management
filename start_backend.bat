@echo off
title Ansh Air Cool - Backend Server
color 0A

echo ========================================
echo   ANSH AIR COOL - BACKEND SERVER
echo ========================================
echo.
echo Starting Flask API Server...
echo.
echo Backend will run on: http://localhost:5000
echo API Docs: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0backend"

if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env and update:
    echo - DATABASE_URL
    echo - API_KEY
    echo - WHATSAPP credentials
    echo.
    pause
)

if not exist "instance" (
    echo Creating database folder...
    mkdir instance
)

echo Starting server...
echo.
python main.py

pause
