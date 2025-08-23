@echo off
REM AI PDF Splitter Pro - Windows Launcher Script
REM Automatic setup and launch for Windows

setlocal enabledelayedexpansion

:: Set colors (if supported)
set "CYAN=[96m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: Get script directory
set "DIR=%~dp0"
cd /d "%DIR%"

echo %CYAN%
echo 🚀 AI PDF Splitter Pro - Intelligent Document Processing Suite
echo ================================================================
echo %NC%

:: Check Python installation
echo %CYAN%[INFO]%NC% Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%NC% Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo %GREEN%[SUCCESS]%NC% Python %PYTHON_VERSION% found

:: Check if virtual environment exists
if not exist "venv" (
    echo %CYAN%[INFO]%NC% Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo %RED%[ERROR]%NC% Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo %GREEN%[SUCCESS]%NC% Virtual environment created
)

:: Activate virtual environment
echo %CYAN%[INFO]%NC% Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%NC% Failed to activate virtual environment!
    pause
    exit /b 1
)

:: Check if requirements are installed
echo %CYAN%[INFO]%NC% Checking dependencies...
python -c "import fitz, google.generativeai, dotenv, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo %CYAN%[INFO]%NC% Installing required dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo %RED%[ERROR]%NC% Failed to install dependencies!
        pause
        exit /b 1
    )
    echo %GREEN%[SUCCESS]%NC% Dependencies installed successfully
) else (
    echo %GREEN%[SUCCESS]%NC% All dependencies are already installed
)

:: Check .env file
if not exist ".env" (
    echo %CYAN%[INFO]%NC% Creating .env configuration file...
    
    (
        echo # AI PDF Splitter Pro Configuration
        echo # ================================
        echo.
        echo # Google Gemini AI API Key
        echo # Get your key from: https://makersuite.google.com/app/apikey
        echo GEMINI_API_KEY=your_api_key_here
        echo.
        echo # AI Model Configuration
        echo GEMINI_TEMPERATURE=0.1
        echo GEMINI_MAX_TOKENS=8192
        echo.
        echo # Processing Settings
        echo MAX_FILE_SIZE_MB=400
        echo COMPRESSION_TARGET_MB=50
    ) > .env
    
    echo %GREEN%[SUCCESS]%NC% .env file created
    echo.
    echo %YELLOW%[WARNING]%NC% 📋 SETUP REQUIRED:
    echo 1. Visit: https://makersuite.google.com/app/apikey
    echo 2. Sign in with your Google account
    echo 3. Create a new API key
    echo 4. Copy the key and paste it in the .env file
    echo.
    echo %CYAN%[INFO]%NC% Opening .env file for editing...
    
    :: Try to open with notepad
    notepad .env
    
    echo.
    echo Please save the .env file after adding your API key and close notepad.
    pause
)

:: Validate API key
findstr /C:"your_api_key_here" .env >nul
if %errorlevel% equ 0 (
    echo %RED%[ERROR]%NC% API key not configured!
    echo Please edit the .env file and add your Google Gemini API key
    echo Run this script again after updating the API key
    pause
    exit /b 1
)

:: Load .env file (simplified)
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    if "%%a"=="GEMINI_API_KEY" set "GEMINI_API_KEY=%%b"
)

if "!GEMINI_API_KEY!"=="" (
    echo %RED%[ERROR]%NC% GEMINI_API_KEY not set in .env file!
    pause
    exit /b 1
)

if "!GEMINI_API_KEY!"=="your_api_key_here" (
    echo %RED%[ERROR]%NC% Please replace 'your_api_key_here' with your actual API key!
    pause
    exit /b 1
)

echo %GREEN%[SUCCESS]%NC% Configuration validated

:: Launch the application
echo.
echo %CYAN%[INFO]%NC% 🚀 Launching AI PDF Splitter Pro...
echo %CYAN%[INFO]%NC% 📁 Project directory: %DIR%
echo %CYAN%[INFO]%NC% 🐍 Python environment: venv
echo %CYAN%[INFO]%NC% 💻 Starting modern GUI interface...
echo.

:: Launch the GUI
python ai_pdf_splitter_gui.py

if %errorlevel% neq 0 (
    echo.
    echo %RED%[ERROR]%NC% Application failed to start!
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo %GREEN%[SUCCESS]%NC% Application closed successfully.
pause
