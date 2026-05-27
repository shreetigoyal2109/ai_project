@echo off
REM AI Project Deployment Setup Script for Windows

echo ========================================
echo AI Interview Platform - Deployment Setup
echo ========================================
echo.

REM Check Python installation
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    exit /b 1
)

echo.
echo [1/6] Creating virtual environment...
python -m venv venv_deploy
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    exit /b 1
)

echo [✓] Virtual environment created

echo.
echo [2/6] Activating virtual environment...
call venv_deploy\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    exit /b 1
)

echo [✓] Virtual environment activated

echo.
echo [3/6] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip, continuing...
)

echo [✓] Pip upgraded

echo.
echo [4/6] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

echo [✓] Dependencies installed

echo.
echo [5/6] Setting up environment variables...
if not exist .env (
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env
    echo [⚠] Created .env - Please edit it with your API keys before running
    echo      - GEMINI_API_KEY
    echo      - OPENAI_API_KEY
    echo      - GROQ_API_KEY
    echo      - DATABASE_URL
    echo      - SECRET_KEY
) else (
    echo [✓] .env file already exists
)

echo.
echo [6/6] Deployment setup complete!

echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Edit .env file with your configuration:
echo    notepad .env
echo.
echo 2. Start the server:
echo    venv_deploy\Scripts\activate.bat
echo    uvicorn main:app --reload
echo.
echo 3. Access the application:
echo    - API: http://localhost:8000
echo    - Documentation: http://localhost:8000/docs
echo.
echo ========================================
pause
