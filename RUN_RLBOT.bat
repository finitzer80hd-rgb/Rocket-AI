@echo off
setlocal
cd /d "%~dp0"
if exist "RocketAIRunner.exe" (
  echo Starting Rocket AI in an RLBot v5 offline match...
  "RocketAIRunner.exe"
  if errorlevel 1 pause
  exit /b
)
if exist "venv\\Scripts\\python.exe" (
  echo Starting source version of Rocket AI...
  "venv\\Scripts\\python.exe" run_rlbot.py
  if errorlevel 1 pause
  exit /b
)
echo Could not find RocketAIRunner.exe or the source venv.
echo For the packaged build, re-download the full RocketAI-Windows-exe artifact.
echo For source, create venv with Python 3.12 and install -e ".[rlbot]".
pause
