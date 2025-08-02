@echo off
echo 🏨 Hotel Management System - Windows Launcher
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install requirements
echo 📦 Installing requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo ✅ Requirements installed
echo.

REM Run the application
echo 🚀 Starting Hotel Management System...
echo ================================================
python main.py

REM If the application exits, show a message
echo.
echo Application closed.
pause
