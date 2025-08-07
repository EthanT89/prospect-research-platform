@echo off
title Prospect Research Platform - Development Environment

echo =====================================
echo  Prospect Research Platform
echo  AI Agent Orchestration Platform
echo =====================================
echo.
echo Starting development environment...
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs  
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C to stop all services
echo =====================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating Python virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Creating from template...
    if exist ".env.example" (
        copy .env.example .env
        echo Please edit .env with your API keys before continuing
        notepad .env
    ) else (
        echo Error: No .env.example template found
        pause
        exit /b 1
    )
)

REM Start backend API server
echo Starting backend API server...
start "Backend API Server" cmd /k "title Backend API && python api\main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend if it exists
if exist "frontend\package.json" (
    echo Starting frontend development server...
    start "Frontend Dev Server" cmd /k "title Frontend Dev && cd frontend && npm run dev"
) else (
    echo Frontend not found - skipping frontend startup
    echo To create frontend: npx create-next-app@latest frontend --typescript --tailwind
)

echo.
echo =====================================
echo Development environment started!
echo =====================================
echo.
echo Available services:
echo  - Backend API: http://localhost:8000
echo  - API Documentation: http://localhost:8000/docs
echo  - Health Check: http://localhost:8000/health
if exist "frontend\package.json" (
    echo  - Frontend: http://localhost:3000
)
echo.
echo This window will remain open for monitoring.
echo Close this window to stop the development environment.
echo =====================================

REM Keep the window open
:loop
timeout /t 30 /nobreak > nul
echo [%time%] Development environment running...
goto loop