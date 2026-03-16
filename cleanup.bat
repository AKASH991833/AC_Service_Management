@echo off
REM ============================================
REM Ansh Air Cool - Cleanup Script
REM Removes test, debug, and check files safely
REM ============================================

echo.
echo ============================================
echo   Ansh Air Cool - Cleanup Script
echo ============================================
echo.

cd /d "E:\WEBISTE UI ADN BAC"

echo [1/4] Cleaning root directory...
del /q check_schema.py 2>nul
del /q quick_check.py 2>nul
echo [OK] Root directory cleaned

echo.
echo [2/4] Cleaning backend directory...
del /q backend\test_api.py 2>nul
del /q backend\test_api2.py 2>nul
del /q backend\test_complete.py 2>nul
del /q backend\test_detailed.py 2>nul
del /q backend\test_direct_db.py 2>nul
del /q backend\test_direct_service_request.py 2>nul
del /q backend\test_form_submit.py 2>nul
del /q backend\test_whatsapp.py 2>nul
del /q backend\check_db.py 2>nul
del /q backend\check_service_requests.py 2>nul
del /q backend\debug_service_request.py 2>nul
echo [OK] Backend directory cleaned

echo.
echo [3/4] Cleaning software directory...
del /q "software for ai creater - Copy\test_login.py" 2>nul
del /q "software for ai creater - Copy\comprehensive_test.py" 2>nul
del /q "software for ai creater - Copy\functional_tests.py" 2>nul
echo [OK] Software directory cleaned

echo.
echo [4/4] Archiving old reports...
if not exist "archive" mkdir "archive"
if not exist "archive\docs" mkdir "archive\docs"
move /y "frontend\AUDIT_REPORT.md" "archive\docs\" 2>nul
if %errorlevel%==0 echo [OK] AUDIT_REPORT.md archived
move /y "software for ai creater - Copy\CLEANUP_REPORT.md" "archive\docs\" 2>nul
if %errorlevel%==0 echo [OK] CLEANUP_REPORT.md archived

echo.
echo ============================================
echo   Cleanup Complete!
echo ============================================
echo.
echo Files deleted:
echo   - 13 test_*.py files
echo   - 3 check_*.py files
echo   - 1 debug_*.py file
echo   - 2 old reports archived
echo.
echo Your project is now cleaner and cleaner!
echo.
pause
