@echo off
echo NBA Lineup Optimizer Launcher
echo ===========================
echo.

REM Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check for pip
python -m pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pip is not installed.
    echo Please install pip and try again.
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

REM Verify streamlit installation
pip show streamlit >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Streamlit not found. Installing directly...
    pip install streamlit
)

REM Run the application using module approach
echo.
echo Starting NBA Lineup Optimizer...
echo.
python -m streamlit run app.py

REM Deactivate virtual environment when app is closed
call venv\Scripts\deactivate

echo.
echo Application closed.
pause 