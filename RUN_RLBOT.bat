@echo off
setlocal
cd /d "%~dp0"
if not exist "venv\\Scripts\\python.exe" (
  echo Missing project virtual environment.
  echo Create it with: py -3.12 -m venv venv
  echo Then run: venv\\Scripts\\python -m pip install -e ".[rlbot]"
  pause
  exit /b 1
)
echo Starting Rocket AI in an RLBot v5 offline match...
"venv\\Scripts\\python.exe" run_rlbot.py
if errorlevel 1 pause
