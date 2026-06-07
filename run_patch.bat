@echo off
setlocal
python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 exit /b %errorlevel%
python "%~dp0clypra_han\apply_clypra_zh.py" %*
pause
