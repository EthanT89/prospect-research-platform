# Scripts

This directory contains development and deployment scripts.

## Structure

- **windows/** - Windows-specific batch scripts
- **setup-dev-env.py** - Cross-platform Python setup script

## Windows Scripts

Located in `windows/`:
- **dev-start.bat** - Start development environment
- **dev-stop.bat** - Stop development services
- **qa-check.bat** - Run code quality checks
- **test-api.bat** - Test API endpoints
- **setup-windows.bat** - Complete Windows setup
- **quick-start-windows.bat** - Quick development startup

## Usage

### Start Development Environment
```cmd
scripts\windows\dev-start.bat
```

### Run Quality Checks
```cmd
scripts\windows\qa-check.bat
```

### Test API
```cmd
scripts\windows\test-api.bat
```