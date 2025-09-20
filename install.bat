@echo off
echo Python Terminal Installation Script
echo ===================================
echo.

REM Check if Python is available
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python from https://python.org
    echo or use the Microsoft Store to install Python.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

REM Install required packages
echo Installing psutil...
pip install psutil

if %errorlevel% neq 0 (
    echo Error installing psutil. Trying with --user flag...
    pip install --user psutil
)

echo.
echo Installation complete!
echo.
echo To run the terminal:
echo   python terminal.py
echo.
echo Or double-click run_terminal.bat
echo.
pause
