@echo off
chcp 65001 >nul
setlocal

where python >nul 2>nul
if errorlevel 1 (
  echo 没有找到 Python。
  echo 请先安装 Python，并在安装时勾选 Add python.exe to PATH。
  pause
  exit /b 1
)

python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
  echo 需要的小组件安装失败，请检查网络后重试。
  pause
  exit /b %errorlevel%
)

python "%~dp0clypra_han\apply_clypra_zh.py" %*
pause
