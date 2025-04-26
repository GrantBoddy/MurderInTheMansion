@echo off
title Murder in the Mansion
color 0A
echo.
echo  ███╗   ███╗██╗   ██╗██████╗ ██████╗ ███████╗██████╗     ██╗███╗   ██╗    ████████╗██╗  ██╗███████╗    ███╗   ███╗ █████╗ ███╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗
echo  ████╗ ████║██║   ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██║████╗  ██║    ╚══██╔══╝██║  ██║██╔════╝    ████╗ ████║██╔══██╗████╗  ██║██╔════╝██║██╔═══██╗████╗  ██║
echo  ██╔████╔██║██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝    ██║██╔██╗ ██║       ██║   ███████║█████╗      ██╔████╔██║███████║██╔██╗ ██║███████╗██║██║   ██║██╔██╗ ██║
echo  ██║╚██╔╝██║██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║       ██║   ██╔══██║██╔══╝      ██║╚██╔╝██║██╔══██║██║╚██╗██║╚════██║██║██║   ██║██║╚██╗██║
echo  ██║ ╚═╝ ██║╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║    ██║██║ ╚████║       ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║  ██║██║ ╚████║███████║██║╚██████╔╝██║ ╚████║
echo  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
echo.
echo  A thrilling murder mystery detective game
echo.
echo  Created by Grant
echo.
echo ========================================================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo To play this game, you need to install Python:
    echo 1. Visit https://www.python.org/downloads/
    echo 2. Download and install Python 3.9 or newer
    echo 3. Make sure to check "Add Python to PATH" during installation
    echo 4. Run this game again after installation
    echo.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
echo Detected Python version: %PYTHON_VERSION%

REM Install required packages
echo Installing required packages...
python -m pip install --upgrade pip --quiet
python -m pip install pygame pyyaml --quiet

echo.
echo All requirements satisfied! Starting the game...
echo.
timeout /t 2 >nul

REM Run the game
python main.py

REM If the game exits with an error, pause so the user can see the error message
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo The game exited with an error. See above for details.
    pause
)
