@echo off
echo NBA Lineup Optimizer - Reset Data
echo =============================
echo.

REM Check if the data directory exists
if exist data (
    echo Removing cached data files...
    del /F /Q data\*.csv
    del /F /Q data\models\*.joblib
    echo Data files cleared.
) else (
    echo No data directory found. Creating it...
    mkdir data\models
)

echo.
echo Reset complete. Run 'start.bat' to start the application with fresh data.
echo.
pause 