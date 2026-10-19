@echo off
setlocal
cd /d "%~dp0"
title Build Rocket AI EXE

echo ========================================
echo   Rocket AI - Windows EXE Builder
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher was not found.
  echo Install Python 3.11 or 3.12 from https://www.python.org/downloads/windows/
  echo Check "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)

py -3.11 --version >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 was not found. Trying Python 3.12...
  py -3.12 --version >nul 2>nul
  if errorlevel 1 (
    echo Install Python 3.11 or 3.12, then run this file again.
    pause
    exit /b 1
  )
  set PYVER=3.12
) else (
  set PYVER=3.11
)

echo [1/5] Creating virtual environment...
py -%PYVER% -m venv .venv
if errorlevel 1 goto fail

echo [2/5] Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto fail

echo [3/5] Installing project dependencies...
".venv\Scripts\python.exe" -m pip install -e .
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 goto fail

echo [4/5] Building executable...
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --windowed --onefile --name RocketAI --collect-all stable_baselines3 --collect-all gymnasium launcher.py
if errorlevel 1 goto fail

echo [5/5] Done!
echo.
echo Your executable is:
echo %CD%\dist\RocketAI.exe
echo.
echo Copy the dist folder or the RocketAI.exe file as needed.
echo Keep the project folder and .venv if you want to use the training commands
echo that call Python modules. The standalone launcher may need the environment
echo available beside it for training, because this is a starter application.
pause
exit /b 0

:fail
echo.
echo Build failed. Read the error above, check your internet connection,
echo and confirm Python 3.11 or 3.12 is installed.
pause
exit /b 1
