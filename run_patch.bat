@echo off
setlocal

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  echo Please install Python and check "Add python.exe to PATH" during setup.
  echo Download: https://www.python.org/downloads/
  pause
  exit /b 1
)

python --version >nul 2>nul
if errorlevel 1 (
  echo Python was found, but it cannot run correctly.
  echo Please reinstall Python and check "Add python.exe to PATH" during setup.
  pause
  exit /b 1
)

python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
  echo Failed to install the required package.
  echo Please check your network and run this file again.
  pause
  exit /b %errorlevel%
)

python "%~dp0clypra_han\apply_clypra_zh.py" %*
set "PATCH_EXIT=%ERRORLEVEL%"
if not "%PATCH_EXIT%"=="0" (
  echo.
  echo Patch failed. Please keep this window open and send a screenshot.
)
pause
exit /b %PATCH_EXIT%
