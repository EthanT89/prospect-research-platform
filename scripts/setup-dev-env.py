#!/usr/bin/env python3
"""
Development environment setup script for Claude Code optimization.
Automates the setup process for new developers and CI/CD.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional

def run_command(cmd: List[str], cwd: Optional[Path] = None) -> bool:
    """Run a command and return success status."""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_prerequisites() -> Dict[str, bool]:
    """Check if required tools are installed."""
    checks = {
        'python': check_python(),
        'node': check_node(),
        'git': check_git(),
    }
    return checks

def check_python() -> bool:
    """Check Python version."""
    try:
        import sys
        version = sys.version_info
        if version.major == 3 and version.minor >= 11:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} found")
            return True
        else:
            print(f"❌ Python 3.11+ required, found {version.major}.{version.minor}")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def check_node() -> bool:
    """Check Node.js version."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} found")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except Exception as e:
        print(f"❌ Node.js check failed: {e}")
        return False

def check_git() -> bool:
    """Check Git installation."""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ {version} found")
            return True
        else:
            print("❌ Git not found")
            return False
    except Exception as e:
        print(f"❌ Git check failed: {e}")
        return False

def setup_python_env() -> bool:
    """Setup Python virtual environment and install dependencies."""
    print("\n🐍 Setting up Python environment...")
    
    # Create virtual environment
    if not Path('venv').exists():
        if not run_command([sys.executable, '-m', 'venv', 'venv']):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Determine Python executable in venv
    if os.name == 'nt':  # Windows
        python_exe = Path('venv/Scripts/python.exe')
        pip_exe = Path('venv/Scripts/pip.exe')
        activate_script = Path('venv/Scripts/activate.bat')
    else:  # Unix-like
        python_exe = Path('venv/bin/python')
        pip_exe = Path('venv/bin/pip')
        activate_script = Path('venv/bin/activate')
    
    # Upgrade pip
    if not run_command([str(pip_exe), 'install', '--upgrade', 'pip']):
        return False
    
    # Install requirements
    if Path('requirements.txt').exists():
        if not run_command([str(pip_exe), 'install', '-r', 'requirements.txt']):
            return False
    
    # Install development dependencies
    if not run_command([str(pip_exe), 'install', '-e', '.[dev]']):
        print("⚠️  Development dependencies installation failed (this is expected if pyproject.toml is not fully configured)")
    
    print("✅ Python environment setup complete")
    return True

def setup_node_env() -> bool:
    """Setup Node.js environment for frontend."""
    print("\n📦 Setting up Node.js environment...")
    
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print("ℹ️  Frontend directory doesn't exist yet - skipping Node.js setup")
        return True
    
    # Install frontend dependencies
    if not run_command(['npm', 'install'], cwd=frontend_dir):
        return False
    
    print("✅ Node.js environment setup complete")
    return True

def setup_git_hooks() -> bool:
    """Setup Git hooks for code quality."""
    print("\n🔧 Setting up Git hooks...")
    
    hooks_dir = Path('.git/hooks')
    if not hooks_dir.exists():
        print("⚠️  Not a Git repository - skipping hooks setup")
        return True
    
    # Create pre-commit hook
    pre_commit_hook = hooks_dir / 'pre-commit'
    hook_content = '''#!/bin/sh
# Pre-commit hook for code quality
set -e

echo "Running pre-commit checks..."

# Python formatting and linting
echo "Checking Python code..."
black --check .
ruff check .
mypy .

# Frontend checks (if frontend exists)
if [ -d "frontend" ]; then
    echo "Checking frontend code..."
    cd frontend
    npm run lint
    npm run type-check
    cd ..
fi

echo "✅ Pre-commit checks passed!"
'''
    
    try:
        with open(pre_commit_hook, 'w') as f:
            f.write(hook_content)
        pre_commit_hook.chmod(0o755)  # Make executable
        print("✅ Git pre-commit hook installed")
        return True
    except Exception as e:
        print(f"⚠️  Failed to setup Git hooks: {e}")
        return True  # Non-critical

def setup_vscode_settings() -> bool:
    """Setup VS Code settings for optimal development."""
    print("\n⚙️  Setting up VS Code configuration...")
    
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    
    # Extensions recommendations
    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.mypy-type-checker", 
            "charliermarsh.ruff",
            "ms-python.black-formatter",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "ms-vscode.vscode-typescript-next"
        ]
    }
    
    try:
        with open(vscode_dir / 'extensions.json', 'w') as f:
            json.dump(extensions, f, indent=2)
        print("✅ VS Code extensions recommendations created")
        return True
    except Exception as e:
        print(f"⚠️  Failed to setup VS Code settings: {e}")
        return True  # Non-critical

def setup_environment_file() -> bool:
    """Setup environment variables file."""
    print("\n🔐 Setting up environment configuration...")
    
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_example.exists() and not env_file.exists():
        try:
            env_file.write_text(env_example.read_text())
            print("✅ Environment file created from template")
            print("⚠️  Please edit .env with your actual API keys and configuration")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    elif env_file.exists():
        print("✅ Environment file already exists")
        return True
    else:
        print("⚠️  No .env.example found - create environment configuration manually")
        return True

def verify_setup() -> bool:
    """Verify the development setup is working."""
    print("\n🧪 Verifying development setup...")
    
    # Test Python imports
    try:
        import sys
        sys.path.append(str(Path.cwd()))
        from config.settings import settings
        print("✅ Configuration system working")
    except ImportError as e:
        print(f"⚠️  Configuration system not ready: {e}")
    
    try:
        from utils.database import db
        print("✅ Database utilities loadable")
    except ImportError as e:
        print(f"⚠️  Database utilities not ready: {e}")
    
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Prospect Research Platform development environment")
    print("=" * 60)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    prereqs = check_prerequisites()
    
    if not all(prereqs.values()):
        print("\n❌ Some prerequisites are missing. Please install them first:")
        for tool, status in prereqs.items():
            if not status:
                print(f"  - {tool}")
        sys.exit(1)
    
    success = True
    
    # Setup steps
    success &= setup_environment_file()
    success &= setup_python_env()
    success &= setup_node_env()
    success &= setup_git_hooks()
    success &= setup_vscode_settings()
    success &= verify_setup()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Development environment setup complete!")
        print("\nNext steps:")
        print("1. Edit .env with your API keys")
        print("2. Run database/schema.sql in Supabase SQL editor")
        print("3. Start development: make dev")
        print("4. Open http://localhost:8000 and http://localhost:3000")
        print("\nFor Claude Code optimization:")
        print("- Install recommended VS Code extensions")
        print("- Setup MCPs using setup-mcps.md")
        print("- Configure Claude Code with .claude-code/mcp-config.json")
    else:
        print("⚠️  Setup completed with some issues. Check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()