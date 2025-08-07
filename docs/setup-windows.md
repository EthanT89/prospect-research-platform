# Windows Setup Guide for Prospect Research Platform

## Prerequisites (Install These First)

### Required Software
1. **Python 3.11+**: Download from [python.org](https://python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Install pip (included by default)

2. **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)
   - ✅ Check "Add to PATH" during installation
   - ✅ npm is included automatically

3. **Git**: Download from [git-scm.com](https://git-scm.com/download/win)
   - ✅ Use recommended settings during installation
   - ✅ Install Git Bash (recommended)

4. **GitHub CLI** (optional but recommended): Download from [cli.github.com](https://cli.github.com/)

### Verify Installation
Open Command Prompt or PowerShell and run:
```cmd
python --version
node --version
npm --version
git --version
gh --version
```

## Step 1: Initialize Repository

### Option A: Using GitHub CLI (Recommended)
```cmd
# Initialize git repository
git init
git branch -M main

# Create GitHub repository
gh repo create prospect-research-platform --public --description "AI agent orchestration platform for B2B sales automation"

# Connect local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/prospect-research-platform.git
```

### Option B: Manual GitHub Setup
1. Go to [github.com/new](https://github.com/new)
2. Create repository named `prospect-research-platform`
3. Make it public
4. Don't initialize with README (we already have one)
5. Copy the repository URL
6. In your project directory:
```cmd
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/prospect-research-platform.git
```

## Step 2: Python Environment Setup

### Create Virtual Environment
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment (Command Prompt)
venv\Scripts\activate

# OR for PowerShell users
venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

### Install Dependencies
```cmd
# Install core dependencies (create requirements.txt first if it doesn't exist)
pip install crewai>=0.28.0
pip install crewai-tools>=0.1.0
pip install fastapi>=0.104.0
pip install uvicorn>=0.24.0
pip install supabase>=2.0.0
pip install python-dotenv>=1.0.0
pip install pydantic>=2.0.0
pip install httpx>=0.25.0
pip install python-json-logger>=2.0.0

# Development dependencies
pip install pytest>=7.4.0
pip install pytest-asyncio>=0.21.0
pip install black>=23.0.0
pip install ruff>=0.1.0
pip install mypy>=1.0.0
pip install coverage>=7.0.0

# Save installed packages
pip freeze > requirements.txt
```

## Step 3: Environment Configuration

### Create Environment File
```cmd
# Copy environment template
copy .env.example .env

# Edit .env with your actual values using notepad or your preferred editor
notepad .env
```

### Required Environment Variables
Add these to your `.env` file:
```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# AI Model Configuration
OPENAI_API_KEY=sk-your_openai_key_here
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

# Web Search (choose one)
SERPER_API_KEY=your_serper_key_here
BRAVE_API_KEY=your_brave_key_here

# Development Settings
LOG_LEVEL=INFO
ENVIRONMENT=development

# API Settings
API_HOST=127.0.0.1
API_PORT=8000
```

## Step 4: Development Tools Setup

### VS Code Configuration (Recommended Editor)
1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install recommended extensions:
   - Python (ms-python.python)
   - Pylance (ms-python.vscode-pylance)
   - Black Formatter (ms-python.black-formatter)
   - Ruff (charliermarsh.ruff)
   - GitLens (eamodio.gitlens)

### PowerShell Execution Policy (If Using PowerShell)
If you encounter execution policy errors:
```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 5: Project Structure Creation

### Create Directory Structure
```cmd
# Create core directories
mkdir agents\research agents\validation agents\context agents\outreach
mkdir tasks\research tasks\validation tasks\context tasks\outreach
mkdir tools\web_search tools\data_processing tools\communication
mkdir crews
mkdir config
mkdir tests\unit tests\integration
mkdir utils
mkdir data\input data\output data\cache
mkdir api
mkdir database
mkdir scripts
mkdir .github\workflows
mkdir .vscode
mkdir .claude-code

# Create core files
echo. > main.py
echo. > config\__init__.py
echo. > config\settings.py
echo. > utils\__init__.py
echo. > utils\logger.py
echo. > utils\database.py
echo. > agents\__init__.py
echo. > api\__init__.py
echo. > api\main.py
```

## Step 6: Test Development Environment

### Test Python Setup
```cmd
# Activate virtual environment
venv\Scripts\activate

# Test Python imports
python -c "import sys; print(f'Python {sys.version}')"
python -c "import crewai; print('CrewAI installed successfully')"
python -c "from config.settings import settings; print('Configuration system working')"
```

### Test API Server
```cmd
# Start the API server
python api\main.py

# In another Command Prompt window, test the API
curl http://localhost:8000/health
# OR use PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

## Step 7: Git Configuration

### Initial Commit
```cmd
# Add all files to git
git add .

# Create initial commit
git commit -m "Initial setup with Windows optimization"

# Push to GitHub
git push -u origin main
```

### Git Configuration (First Time Setup)
```cmd
# Set your Git identity (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Optional: Set default editor
git config --global core.editor "code --wait"
```

## Step 8: Frontend Setup (Optional)

### Create Next.js Frontend
```cmd
# Create frontend directory
mkdir frontend
cd frontend

# Initialize Next.js project
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Install additional dependencies
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs

# Return to project root
cd ..
```

## Step 9: Development Workflow Scripts

### Create Batch Files for Common Tasks
```cmd
# Create dev-start.bat
echo @echo off > dev-start.bat
echo echo Starting Prospect Research Platform... >> dev-start.bat
echo echo Backend: http://localhost:8000 >> dev-start.bat
echo echo Frontend: http://localhost:3000 >> dev-start.bat
echo echo Press Ctrl+C to stop >> dev-start.bat
echo. >> dev-start.bat
echo venv\Scripts\activate >> dev-start.bat
echo start "Backend API" python api\main.py >> dev-start.bat
echo start "Frontend" cmd /k "cd frontend && npm run dev" >> dev-start.bat
echo pause >> dev-start.bat
```

### Create Quality Assurance Script
```cmd
# Create qa-check.bat
echo @echo off > qa-check.bat
echo echo Running quality assurance checks... >> qa-check.bat
echo venv\Scripts\activate >> qa-check.bat
echo echo Formatting code... >> qa-check.bat
echo black . >> qa-check.bat
echo echo Linting code... >> qa-check.bat
echo ruff check . >> qa-check.bat
echo echo Type checking... >> qa-check.bat
echo mypy . >> qa-check.bat
echo echo Running tests... >> qa-check.bat
echo pytest >> qa-check.bat
echo echo Quality checks complete! >> qa-check.bat
echo pause >> qa-check.bat
```

## Step 10: Verify Complete Setup

### Final Verification Commands
```cmd
# Activate virtual environment
venv\Scripts\activate

# Test configuration loading
python -c "from config.settings import settings; print('✅ Configuration loaded')"

# Test database utilities
python -c "from utils.database import db; print('✅ Database utilities ready')"

# Test API health
python api\main.py
# In another window: curl http://localhost:8000/health
```

## Troubleshooting Common Windows Issues

### Issue: "python" not recognized
**Solution**: Reinstall Python and check "Add Python to PATH"

### Issue: Virtual environment activation fails
**Solution**: Use full path:
```cmd
C:\Coding\prospect-research\venv\Scripts\activate
```

### Issue: PowerShell script execution blocked
**Solution**: Change execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port already in use
**Solution**: Kill process or change port:
```cmd
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue: Long file paths
**Solution**: Enable long paths in Windows:
1. Run `gpedit.msc` as administrator
2. Navigate to: Computer Configuration > Administrative Templates > System > Filesystem
3. Enable "Enable Win32 long paths"

## Next Steps
1. ✅ Setup Supabase database (run database/schema.sql)
2. ✅ Configure API keys in .env
3. ✅ Setup MCPs for Claude Code (see MCP setup guide)
4. ✅ Start development with `dev-start.bat`
5. ✅ Begin building your first AI agent