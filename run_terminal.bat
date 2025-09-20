@echo off
echo Python Terminal Launcher
echo ========================

REM Try different Python commands
echo Attempting to start Python Terminal...

REM Try python command
python terminal.py 2>nul
if %errorlevel% equ 0 goto :end

REM Try python3 command  
python3 terminal.py 2>nul
if %errorlevel% equ 0 goto :end

REM Try py command
py terminal.py 2>nul
if %errorlevel% equ 0 goto :end

REM If all fail, show error
echo.
echo Error: Python not found or not properly installed.
echo.
echo Please install Python from https://python.org
echo or use the Microsoft Store to install Python.
echo.
echo After installing Python, run:
echo   pip install psutil
echo.
echo Then try running this script again.
echo.
pause

:end
