@echo off
REM ============================================================================
REM AI-Based Student Performance & Risk Prediction System
REM Automated Windows Setup & Launch Script
REM B.Tech Second-Year Mini-Project
REM ============================================================================

setlocal enabledelayedexpansion
title AI Student Risk Prediction System - Setup & Launcher

echo ============================================================================
echo   AI-Based Student Performance & Risk Prediction System
echo   B.Tech Second-Year Mini-Project Launcher
echo ============================================================================
echo.

REM 1. Check Python installation
echo [1/6] Verifying Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.11+ and ensure "Add Python to PATH" is checked.
    pause
    exit /b 1
)
python --version

REM 2. Create or verify virtual environment (optional/safe check)
if not exist "venv" (
    echo [2/6] Virtual environment not detected. Creating venv...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] Could not create virtual environment. Continuing with system Python...
    ) else (
        echo [INFO] Virtual environment created successfully.
    )
)

if exist "venv\Scripts\activate.bat" (
    echo [2/6] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [2/6] Using current Python environment...
)

REM 3. Install dependencies from requirements.txt
echo [3/6] Installing/verifying required dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install required packages!
    pause
    exit /b 1
)

REM 4. Generate synthetic dataset if not present
if not exist "ml\dataset\students.csv" (
    echo [4/6] Dataset not found. Generating synthetic academic dataset (1,200 records)...
    python ml\generate_dataset.py
) else (
    echo [4/6] Dataset verified at ml\dataset\students.csv.
)

REM 5. Train Decision Tree model if missing
if not exist "ml\models\risk_model.pkl" (
    echo [5/6] ML Model not found. Training DecisionTreeClassifier pipeline...
    python ml\train_model.py
) else (
    echo [5/6] ML Model verified at ml\models\risk_model.pkl.
)

REM 6. Launch the Flask Web Application
echo.
echo ============================================================================
echo [6/6] Launching Application Server...
echo Portal URL: http://127.0.0.1:5000
echo Press Ctrl+C in this terminal window to stop the server.
echo ============================================================================
echo.

python app.py
pause
