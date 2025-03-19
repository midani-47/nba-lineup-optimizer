@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo    NBA Lineup Optimizer - Startup Script (Windows)
echo ===================================================
echo.

REM Check Python version
echo Checking Python version...
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
if not defined PYTHON_VERSION (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
echo Found Python version: %PYTHON_VERSION%
echo Python version check passed.
echo.

REM Check Node.js version
echo Checking Node.js version...
for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
if not defined NODE_VERSION (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 14 or higher
    pause
    exit /b 1
)
echo Found Node.js version: %NODE_VERSION%
echo Node.js version check passed.
echo.

REM Clean old log files
echo Cleaning old log files...
if exist "backend\backend_log.txt" del "backend\backend_log.txt"
if exist "frontend\frontend_log.txt" del "frontend\frontend_log.txt"
echo.

REM Function to check if a port is in use
:check_port
set "port=%1"
netstat -ano | find ":%port%" >nul 2>&1
if %errorlevel% equ 0 (
    set /a port+=1
    goto check_port
)
set "available_port=%port%"
goto :eof

REM Find available ports
echo Checking if required ports are available...
set "frontend_port=3000"
set "backend_port=8000"

call :check_port %frontend_port%
set "frontend_port=%available_port%"

call :check_port %backend_port%
set "backend_port=%available_port%"

echo Using frontend port: %frontend_port%
echo Using backend port: %backend_port%
echo.

REM Set environment variables for ports
set "PORT=%frontend_port%"
set "BACKEND_PORT=%backend_port%"

REM Check and create virtual environment if needed
echo Checking virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv --clear
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        echo Please make sure you have the venv module installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Check and fix database
echo Checking database...
cd backend
python fix_data.py
if %errorlevel% neq 0 (
    echo [WARNING] Database fix encountered issues
    echo Trying to continue anyway...
)

REM Apply migrations
echo Applying database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to apply migrations
    cd ..
    pause
    exit /b 1
)

cd ..

REM Start backend server
echo Starting backend server...
start "Backend Server" cmd /c "cd backend && python manage.py runserver 0.0.0.0:%backend_port% > backend_log.txt 2>&1"

REM Wait for backend to initialize
echo Waiting for backend server to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend server
echo Starting frontend server...
start "Frontend Server" cmd /c "cd frontend && set PORT=%frontend_port% && npm start > frontend_log.txt 2>&1"

echo.
echo ===================================================
echo    NBA Lineup Optimizer is now running!
echo    Backend API: http://localhost:%backend_port%/api/
echo    Frontend UI: http://localhost:%frontend_port%/
echo ===================================================
echo.
echo Press Ctrl+C to shut down both servers
echo.

REM Keep the window open
pause 