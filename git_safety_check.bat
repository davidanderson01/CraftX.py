@echo off
REM Git Safety Check Script
REM Run this periodically to ensure Git is safely configured

echo ========================================
echo Git Safety Check
echo ========================================

cd /d "C:\Users\david\CraftXPy\CraftX.py"

echo Checking for dangerous Git repository in user directory...
if exist "C:\Users\david\.git" (
    echo WARNING: Found .git in user directory!
    echo Run prevent_git_user_repo.py to fix this issue
    pause
    exit /b 1
) else (
    echo OK: No .git found in user directory
)

echo.
echo Checking Git repository status...
git status --porcelain
if %ERRORLEVEL% neq 0 (
    echo ERROR: Git status failed
    pause
    exit /b 1
)

echo.
echo Verifying Git repository root...
git rev-parse --show-toplevel
if %ERRORLEVEL% neq 0 (
    echo ERROR: Cannot determine Git repository root
    pause
    exit /b 1
)

echo.
echo ========================================
echo All Git safety checks passed!
echo ========================================
pause
