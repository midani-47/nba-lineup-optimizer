@echo off
echo.
echo ===================================================
echo    NBA Lineup Optimizer - Startup Script (Windows)
echo ===================================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    goto :end
)

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16 or higher and try again
    goto :end
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
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
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some dependencies may not have installed correctly
)

REM Check and fix database
echo.
echo Checking database...
cd backend
python check_db.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Database check encountered issues
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