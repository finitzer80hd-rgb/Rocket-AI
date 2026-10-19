@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Python environment not found.
  echo First run BUILD_EXE_WINDOWS.bat to install dependencies and build the launcher.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" launcher.py
