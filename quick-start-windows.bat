@echo off
title Quick Start - Prospect Research Platform

echo =====================================
echo  Quick Start Guide
echo  Prospect Research Platform
echo =====================================
echo.
echo This will get you up and running in 5 minutes!
echo.

REM Check if setup has been run
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Setup not completed yet!
    echo.
    echo Please run setup-windows.bat first to configure your environment.
    echo.
    pause
    exit /b 1
)

echo [1/5] Activating Python environment...
call venv\Scripts\activate.bat
echo ✅ Python environment activated
echo.

echo [2/5] Checking environment configuration...
if not exist ".env" (
    echo ⚠️ No .env file found - creating template...
    copy .env.example .env 2>nul || (
        echo SUPABASE_URL=https://your-project.supabase.co > .env
        echo OPENAI_API_KEY=sk-your-key-here >> .env
    )
    echo.
    echo ⚠️ Please edit .env with your actual API keys:
    notepad .env
    echo.
    echo After editing .env, press any key to continue...
    pause >nul
)
echo ✅ Environment configuration found
echo.

echo [3/5] Testing Python dependencies...
python -c "import crewai, fastapi, supabase; print('✅ Core dependencies loaded')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ⚠️ Dependencies missing - installing...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to install dependencies
        echo Please run setup-windows.bat first
        pause
        exit /b 1
    )
)
echo ✅ Dependencies ready
echo.

echo [4/5] Testing configuration...
python -c "from config.settings import settings; print('✅ Configuration system working')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ⚠️ Configuration test failed - this is normal if files don't exist yet
    echo We'll create the basic structure...
    
    REM Create basic config structure
    echo from pydantic import BaseSettings > config\settings.py
    echo. >> config\settings.py
    echo class Settings(BaseSettings): >> config\settings.py
    echo     supabase_url: str = "https://example.supabase.co" >> config\settings.py
    echo     class Config: >> config\settings.py
    echo         env_file = ".env" >> config\settings.py
    echo. >> config\settings.py
    echo settings = Settings() >> config\settings.py
    
    echo ✅ Basic configuration created
)
echo.

echo [5/5] Starting development environment...
echo.
echo =====================================
echo  🚀 Starting Development Environment
echo =====================================
echo.
echo Services starting:
echo  - Backend API: http://localhost:8000
echo  - API Documentation: http://localhost:8000/docs
echo  - Health Check: http://localhost:8000/health
echo.
echo Opening in 3 seconds...
timeout /t 3 /nobreak > nul

REM Start the API server
start "Backend API Server" cmd /k "title Backend API - Prospect Research && python api\main.py"

REM Wait for server to start
echo Waiting for API server to start...
timeout /t 5 /nobreak > nul

REM Test if server is running
curl -s http://localhost:8000/health >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ API server is running!
    
    REM Open documentation in browser
    start http://localhost:8000/docs
    
    echo.
    echo =====================================
    echo  🎉 Quick Start Complete!
    echo =====================================
    echo.
    echo Your development environment is ready:
    echo.
    echo  🌐 API Server: http://localhost:8000
    echo  📚 API Docs: http://localhost:8000/docs
    echo  🏥 Health Check: http://localhost:8000/health
    echo.
    echo Test the API:
    echo  curl http://localhost:8000/health
    echo.
    echo Next steps:
    echo  1. Configure Supabase credentials in .env
    echo  2. Run database\schema.sql in Supabase SQL editor
    echo  3. Set up Claude Code MCPs (see setup-mcps.md)
    echo  4. Start building your first AI agent!
    echo.
    echo Commands:
    echo  dev-start.bat  - Start full development environment
    echo  qa-check.bat   - Run quality assurance checks
    echo  test-api.bat   - Test all API endpoints
    echo =====================================
    
) else (
    echo ❌ Failed to start API server
    echo.
    echo Troubleshooting:
    echo  1. Check if Python is installed correctly
    echo  2. Ensure virtual environment is activated
    echo  3. Verify all dependencies are installed
    echo  4. Check if port 8000 is available
    echo.
    echo Try running: setup-windows.bat
)

echo.
echo This window will close in 30 seconds or press any key to close now...
timeout /t 30 > nul