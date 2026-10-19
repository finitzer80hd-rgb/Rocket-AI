@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo First run BUILD_EXE_WINDOWS.bat to create the environment.
  pause
  exit /b 1
)
echo This installs CUDA-enabled PyTorch for a compatible NVIDIA setup.
echo It does not install NVIDIA drivers. Update your NVIDIA driver first if needed.
echo.
".venv\Scripts\python.exe" -m pip uninstall -y torch torchvision torchaudio
".venv\Scripts\python.exe" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m rocket_ai.tools.check_torch
pause
exit /b 0
:fail
echo PyTorch CUDA installation failed. Use https://pytorch.org/get-started/locally/ to select a compatible build.
pause
exit /b 1
