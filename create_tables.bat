@echo off
title Create Database Tables
color 0A

echo ========================================
echo   Creating New Database Tables
echo ========================================
echo.

cd /d "%~dp0backend"

echo Creating tables for:
echo   - Testimonials
echo   - Services
echo   - Products (AC Sale & Rent)
echo   - Website Content
echo.

python create_new_tables.py

echo.
echo ========================================
echo   Tables Created Successfully!
echo ========================================
echo.

pause
