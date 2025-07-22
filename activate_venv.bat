@echo off
:: Batch file to activate Python venv in a new CMD window
title MyEnv Virtual Environment

:: Path to your virtual environment (adjust if needed)
set "VENV_PATH=myenv"

:: Check if the venv exists
if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Error: Virtual environment not found at "%VENV_PATH%"
    pause
    exit /b 1
)

:: Start a new CMD window with venv activated
cmd /k "%VENV_PATH%\Scripts\activate.bat && echo Virtual Environment '%VENV_PATH%' is now active!"