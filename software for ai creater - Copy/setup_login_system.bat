@echo off
echo ============================================================
echo   LOGIN SYSTEM SETUP - Ansh Air Cool Billing Software
echo ============================================================
echo.
echo This script will update your database with login security features
echo.
echo Press any key to continue...
pause > nul
echo.

echo [1/2] Running database migration...
python database\migrate_login_security.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Database migration completed!
    echo ============================================================
    echo.
    echo Next steps:
    echo 1. Review LOGIN_SYSTEM_README.md for detailed instructions
    echo 2. Test login system with username: admin, password: admin123
    echo 3. Change default password immediately after first login
    echo.
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo [ERROR] Migration failed!
    echo ============================================================
    echo.
    echo Please check:
    echo 1. Database connection settings in config.py
    echo 2. MySQL server is running
    echo 3. Database 'ac_service_billing' exists
    echo.
    echo ============================================================
)

echo.
pause
