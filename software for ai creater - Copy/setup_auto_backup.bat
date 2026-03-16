@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo   SETTING UP DAILY AUTO BACKUP
echo ============================================================
echo.
echo This will create a scheduled task to backup your database
echo every day at 11:00 PM (23:00).
echo.
echo Backup Location: E:\PROJECT_ROOT\backups\
echo Keep Backups For: 30 days
echo.
pause

schtasks /create /tn "AnshAirCool_DailyBackup" /tr "\"E:\PROJECT_ROOT\software for ai creater - Copy\backup_daily.bat\"" /sc daily /st 23:00 /ru SYSTEM /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
echo   [OK] Scheduled task created successfully!
    echo ============================================================
    echo.
    echo Task Name: AnshAirCool_DailyBackup
    echo Schedule: Daily at 11:00 PM
    echo.
    echo To view or modify:
    echo   1. Open Task Scheduler
    echo   2. Find "AnshAirCool_DailyBackup" in the list
    echo.
) else (
    echo.
    echo ============================================================
    echo   [ERROR] Failed to create scheduled task
    echo ============================================================
    echo.
    echo Please run this file as Administrator
    echo.
)

echo.
pause
