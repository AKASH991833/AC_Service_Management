@echo off
echo ========================================
echo   Project Cleanup Script
echo ========================================
echo.

:: Delete Python cache folders
echo [1/8] Deleting Python cache folders...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

:: Delete $null file
echo [2/8] Deleting $null file...
del /q "$null" 2>nul

:: Delete archived CSS files
echo [3/8] Deleting archived CSS files...
del /q "frontend\css\archive\enhanced-effects.css" 2>nul
del /q "frontend\css\archive\premium-design.css" 2>nul

:: Delete old documentation files
echo [4/8] Deleting old documentation...
del /q "frontend\REMAINING_UPGRADES.md" 2>nul
del /q "frontend\UPGRADE_SUMMARY.md" 2>nul

:: Delete empty folders (if empty)
echo [5/8] Cleaning empty folders...
rd /q "software for ai creater - Copy\backups" 2>nul
rd /q "software for ai creater - Copy\logs" 2>nul

:: Delete old audit report
echo [6/8] Deleting old audit reports...
del /q "archive\docs\AUDIT_REPORT.md" 2>nul

:: Cleanup complete
echo.
echo ========================================
echo   Cleanup Complete!
echo ========================================
echo.
pause
