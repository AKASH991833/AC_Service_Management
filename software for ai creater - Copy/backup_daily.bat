@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo   ANSH AIR COOL - DAILY AUTO BACKUP
echo ============================================================
echo.

cd /d "E:\PROJECT_ROOT\software for ai creater - Copy"
python auto_backup.py

echo.
echo Backup completed!
echo Press any key to exit...
pause >nul
exit
