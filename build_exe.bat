@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher (py) not found. Install Python 3.10+ from python.org and enable Add Python to PATH.
  pause
  exit /b 1
)
py -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
  echo Dependency installation failed.
  pause
  exit /b 1
)
py -m PyInstaller --noconfirm --clean --onefile --windowed --name ScreenDot main.py
if errorlevel 1 (
  echo EXE build failed.
  pause
  exit /b 1
)
echo.
echo Ready: dist\ScreenDot.exe
pause
