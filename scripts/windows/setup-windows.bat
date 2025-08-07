@echo off
title Prospect Research Platform - Windows Setup

echo =====================================
echo  Prospect Research Platform Setup
echo  AI Agent Orchestration Platform  
echo =====================================
echo.
echo This script will set up your Windows development environment.
echo Please ensure you have Python 3.11+, Node.js 18+, and Git installed.
echo.
echo Press any key to continue or Ctrl+C to abort...
pause >nul
echo.

REM Check prerequisites
echo [1/8] Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Please install Python 3.11+ from python.org
    pause
    exit /b 1
) else (
    echo ✅ Python found:
    python --version
)

REM Check Node.js
node --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Node.js not found! Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
) else (
    echo ✅ Node.js found:
    node --version
)

REM Check Git
git --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Git not found! Please install Git from git-scm.com
    pause
    exit /b 1
) else (
    echo ✅ Git found:
    git --version
)

echo.
echo [2/8] Creating project directory structure...

REM Create directories
mkdir agents\research agents\validation agents\context agents\outreach 2>nul
mkdir tasks\research tasks\validation tasks\context tasks\outreach 2>nul
mkdir tools\web_search tools\data_processing tools\communication 2>nul
mkdir crews 2>nul
mkdir config 2>nul
mkdir tests\unit tests\integration 2>nul
mkdir utils 2>nul
mkdir data\input data\output data\cache 2>nul
mkdir api 2>nul
mkdir database 2>nul
mkdir scripts 2>nul
mkdir .github\workflows 2>nul
mkdir .vscode 2>nul
mkdir .claude-code 2>nul

REM Create __init__.py files for Python packages
echo. > config\__init__.py
echo. > utils\__init__.py
echo. > agents\__init__.py
echo. > api\__init__.py
echo. > crews\__init__.py
echo. > tasks\__init__.py
echo. > tools\__init__.py

echo ✅ Directory structure created

echo.
echo [3/8] Setting up Python virtual environment...

REM Create virtual environment
if exist "venv" (
    echo ✅ Virtual environment already exists
) else (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    ) else (
        echo ✅ Virtual environment created
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

echo.
echo [4/8] Installing Python dependencies...

REM Upgrade pip
python -m pip install --upgrade pip
echo ✅ pip upgraded

REM Install core dependencies
echo Installing core dependencies...
pip install crewai>=0.28.0 crewai-tools>=0.1.0 fastapi>=0.104.0 uvicorn>=0.24.0
pip install supabase>=2.0.0 python-dotenv>=1.0.0 pydantic>=2.0.0 httpx>=0.25.0
pip install python-json-logger>=2.0.0

REM Install development dependencies
echo Installing development dependencies...
pip install pytest>=7.4.0 pytest-asyncio>=0.21.0 black>=23.0.0
pip install ruff>=0.1.0 mypy>=1.0.0 coverage>=7.0.0

echo ✅ Python dependencies installed

echo.
echo [5/8] Setting up environment configuration...

REM Create .env from template if it doesn't exist
if exist ".env" (
    echo ✅ Environment file already exists
) else (
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Environment file created from template
    ) else (
        echo Creating basic .env template...
        (
        echo # Supabase Configuration
        echo SUPABASE_URL=https://your-project.supabase.co
        echo SUPABASE_ANON_KEY=your_anon_key_here
        echo SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
        echo.
        echo # AI Model Configuration  
        echo OPENAI_API_KEY=sk-your_openai_key_here
        echo ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here
        echo.
        echo # Web Search
        echo SERPER_API_KEY=your_serper_key_here
        echo.
        echo # Development Settings
        echo LOG_LEVEL=INFO
        echo ENVIRONMENT=development
        echo API_HOST=127.0.0.1
        echo API_PORT=8000
        ) > .env
        echo ✅ Basic .env template created
    )
)

echo.
echo [6/8] Setting up Git repository...

REM Initialize git if not already done
if exist ".git" (
    echo ✅ Git repository already initialized
) else (
    git init
    git branch -M main
    echo ✅ Git repository initialized
)

REM Create .gitignore if it doesn't exist
if not exist ".gitignore" (
    (
    echo # Python
    echo __pycache__/
    echo *.py[cod]
    echo venv/
    echo .env
    echo *.log
    echo.
    echo # Node.js
    echo node_modules/
    echo .next/
    echo.
    echo # IDE
    echo .vscode/
    echo .idea/
    echo.
    echo # OS
    echo .DS_Store
    echo Thumbs.db
    echo.
    echo # Temporary files
    echo temp-instructions.md
    echo *.tmp
    ) > .gitignore
    echo ✅ .gitignore created
) else (
    echo ✅ .gitignore already exists
)

echo.
echo [7/8] Setting up Claude Code optimization...

REM Create Claude Code settings if they don't exist
if not exist ".claude-code\settings.json" (
    (
    echo {
    echo   "projectSettings": {
    echo     "name": "Prospect Research Platform",
    echo     "type": "ai-agent-platform",
    echo     "primaryLanguage": "python",
    echo     "framework": "crewai"
    echo   },
    echo   "developmentWorkflow": {
    echo     "testCommand": "pytest",
    echo     "lintCommand": "ruff check .",
    echo     "formatCommand": "black .",
    echo     "startCommand": "python api\\main.py"
    echo   }
    echo }
    ) > .claude-code\settings.json
    echo ✅ Claude Code settings created
) else (
    echo ✅ Claude Code settings already exist
)

echo.
echo [8/8] Creating development shortcuts...

REM Save current requirements
pip freeze > requirements.txt
echo ✅ requirements.txt updated

echo ✅ Windows development environment setup complete!

echo.
echo =====================================
echo  Setup Complete! 
echo =====================================
echo.
echo What was installed:
echo  ✅ Python virtual environment
echo  ✅ AI agent development dependencies
echo  ✅ Code quality tools (Black, Ruff, MyPy)
echo  ✅ Testing framework (pytest)
echo  ✅ Project structure
echo  ✅ Development scripts
echo.
echo Next steps:
echo  1. Edit .env with your API keys (Supabase, OpenAI, etc.)
echo  2. Set up Supabase database (run database\schema.sql)
echo  3. Configure Claude Code MCPs (see setup-mcps.md)
echo  4. Start development: dev-start.bat
echo.
echo Available commands:
echo  dev-start.bat    - Start development environment
echo  dev-stop.bat     - Stop development environment
echo  qa-check.bat     - Run code quality checks
echo  test-api.bat     - Test API endpoints
echo.
echo For Claude Code optimization:
echo  - Follow setup-mcps.md for MCP configuration
echo  - See CLAUDE.md for development patterns
echo  - Use setup-windows.md for detailed instructions
echo.
echo Happy coding! 🚀
echo =====================================
echo.
pause