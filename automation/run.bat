@echo off
REM Personal OS - Windows Launcher Script

echo.
echo ========================================
echo   Personal OS - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo.
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    echo Run: copy .env.example .env
    echo Then edit .env with your API keys.
    echo.
    pause
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Run the application
echo.
echo Starting Personal OS...
echo Press Ctrl+C to stop
echo.
python main.py

pause
