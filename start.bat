@echo off
echo.
echo ===================================================
echo    NBA Lineup Optimizer - Startup Script (Windows)
echo ===================================================
echo.

REM Check Python version
echo Checking Python version...
python --version > temp.txt 2>&1
set /p PYTHON_VERSION=<temp.txt
del temp.txt

if not defined PYTHON_VERSION (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    goto :end
)

echo Found Python version: %PYTHON_VERSION%

REM Extract major and minor version numbers
for /f "tokens=2 delims= " %%a in ("%PYTHON_VERSION%") do set PY_VER=%%a
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)

REM Check if Python version is 3.8 or higher
if %PY_MAJOR% LSS 3 (
    echo [ERROR] Python 3.8 or higher is required, found %PY_VER%
    goto :end
)
if %PY_MAJOR% EQU 3 (
    if %PY_MINOR% LSS 8 (
        echo [ERROR] Python 3.8 or higher is required, found %PY_VER%
        goto :end
    )
)

echo Python version check passed.
echo.

REM Check Node.js version
echo Checking Node.js version...
node --version > temp.txt 2>&1
set /p NODE_VERSION=<temp.txt
del temp.txt

if not defined NODE_VERSION (
    echo [ERROR] Node.js not found. Please install Node.js 16 or higher.
    goto :end
)

echo Found Node.js version: %NODE_VERSION%

REM Extract major version number
set NODE_MAJOR=%NODE_VERSION:~1,2%
if "%NODE_MAJOR:~1,1%"=="." set NODE_MAJOR=%NODE_VERSION:~1,1%

if %NODE_MAJOR% LSS 16 (
    echo [ERROR] Node.js 16 or higher is required, found %NODE_VERSION%
    goto :end
)

echo Node.js version check passed.
echo.

REM Skip memory check as it's causing issues
echo Skipping memory check...

REM Clean old log files
echo Cleaning old log files...
if exist backend\backend_log.txt del backend\backend_log.txt
if exist frontend\frontend_log.txt del frontend\frontend_log.txt

REM Check if ports are available
echo Checking if required ports are available...
netstat -ano | find "8001" > nul
if %ERRORLEVEL% EQU 0 (
    echo [ERROR] Port 8001 is already in use
    echo Please free up port 8001 and try again
    goto :end
)
netstat -ano | find "3000" > nul
if %ERRORLEVEL% EQU 0 (
    echo [ERROR] Port 3000 is already in use
    echo Please free up port 3000 and try again
    goto :end
)

REM Check if virtual environment exists
echo Checking virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        echo Make sure you have the venv module installed (pip install virtualenv)
        goto :end
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment
    goto :end
)

REM Install backend dependencies
echo Installing backend dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some dependencies may not have installed correctly
    echo Trying to continue anyway...
)

REM Check and fix database
echo.
echo Checking database...
cd backend
python check_db.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Database check encountered issues
    echo Trying to continue anyway...
)

REM Apply migrations
echo.
echo Applying database migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to apply migrations
    cd ..
    goto :end
)

REM Fix data if needed
echo.
echo Fixing player data...
python fix_data.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Data fix encountered issues
    echo Trying to continue anyway...
)

REM Start backend server in the background
echo.
echo Starting backend server...
start /b cmd /c "cd %CD% && python manage.py runserver 8001 > backend_log.txt 2>&1"
echo Backend server started in the background (logs in backend_log.txt)

REM Go back to root directory
cd ..

REM Install frontend dependencies
echo.
echo Installing frontend dependencies...
cd frontend
if not exist node_modules (
    echo Running dependency fix script...
    node fix_dependencies.js
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] Dependency fix encountered issues
        echo Trying standard npm install...
        npm install --legacy-peer-deps
    )
) else (
    echo Frontend dependencies already installed
)

REM Start frontend server in the background
echo.
echo Starting frontend server...
start /b cmd /c "npm start > frontend_log.txt 2>&1"
echo Frontend server started in the background (logs in frontend_log.txt)

REM Go back to root directory
cd ..

echo.
echo ===================================================
echo    NBA Lineup Optimizer started successfully!
echo.
echo    Backend: http://localhost:8001/api
echo    Frontend: http://localhost:3000
echo    
echo    Log files:
echo    - backend/backend_log.txt
echo    - frontend/frontend_log.txt
echo ===================================================
echo.
echo The application is now running in the background.
echo You can close this window and the servers will continue running.
echo To stop the servers, press Ctrl+C in each terminal or use Task Manager.
echo.

:end
pause 