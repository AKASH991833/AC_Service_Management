@echo off
REM ========================================
REM ANSH AIR COOL - CLEANUP DUPLICATE FILES
REM Removes redundant and test files from codebase
REM ========================================

echo.
echo ========================================
echo ANSH AIR COOL - FILE CLEANUP
echo ========================================
echo.
echo This script will remove redundant files:
echo - Test files in production
echo - One-time migration scripts (already executed)
echo - Duplicate/obsolete files
echo.
echo Files will be moved to: _deleted_files_backup
echo.
pause

REM Create backup directory
set BACKUP_DIR=_deleted_files_backup
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
echo.
echo [1/3] Creating backup directory...

REM ========================================
REM BACKEND FILES TO REMOVE
REM ========================================
echo.
echo [2/3] Moving backend files to backup...

REM Test files
if exist "backend\quick_test.py" (
    echo   - Moving quick_test.py...
    move /Y "backend\quick_test.py" "%BACKUP_DIR%\"
)

if exist "backend\test_data.py" (
    echo   - Moving test_data.py...
    move /Y "backend\test_data.py" "%BACKUP_DIR%\"
)

REM One-time migration scripts (already executed)
if exist "backend\create_gallery_table.py" (
    echo   - Moving create_gallery_table.py...
    move /Y "backend\create_gallery_table.py" "%BACKUP_DIR%\"
)

if exist "backend\create_new_tables.py" (
    echo   - Moving create_new_tables.py...
    move /Y "backend\create_new_tables.py" "%BACKUP_DIR%\"
)

if exist "backend\fix_service_requests_table.py" (
    echo   - Moving fix_service_requests_table.py...
    move /Y "backend\fix_service_requests_table.py" "%BACKUP_DIR%\"
)

REM Redundant migration scripts
if exist "backend\migrate_admin.py" (
    echo   - Moving migrate_admin.py...
    move /Y "backend\migrate_admin.py" "%BACKUP_DIR%\"
)

if exist "backend\migrate_customers.py" (
    echo   - Moving migrate_customers.py...
    move /Y "backend\migrate_customers.py" "%BACKUP_DIR%\"
)

if exist "backend\migrate_db.py" (
    echo   - Moving migrate_db.py...
    move /Y "backend\migrate_db.py" "%BACKUP_DIR%\"
)

if exist "backend\migrate_service_requests.py" (
    echo   - Moving migrate_service_requests.py...
    move /Y "backend\migrate_service_requests.py" "%BACKUP_DIR%\"
)

REM ========================================
REM FRONTEND FILES TO REMOVE
REM ========================================
echo.
echo [3/3] Moving frontend files to backup...

REM Admin redirect file (redundant)
if exist "frontend\admin\index.html" (
    echo   - Moving frontend\admin\index.html...
    move /Y "frontend\admin\index.html" "%BACKUP_DIR%\"
)

echo.
echo ========================================
echo CLEANUP COMPLETE!
echo ========================================
echo.
echo Removed files are now in: %BACKUP_DIR%
echo.
echo You can safely delete the backup folder after
echo confirming the website works correctly.
echo.
pause
