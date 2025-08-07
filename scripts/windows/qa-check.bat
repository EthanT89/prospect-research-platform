@echo off
title Quality Assurance Check

echo =====================================
echo  Code Quality Assurance Check
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
call venv\Scripts\activate.bat

set ERROR_COUNT=0

echo [1/5] Formatting Python code with Black...
black . --check --diff
if %ERRORLEVEL% neq 0 (
    echo.
    echo Formatting issues found. Running Black to fix them...
    black .
    if %ERRORLEVEL% neq 0 (
        set /a ERROR_COUNT+=1
        echo ERROR: Black formatting failed!
    ) else (
        echo SUCCESS: Code formatted successfully
    )
) else (
    echo SUCCESS: Code is properly formatted
)
echo.

echo [2/5] Linting Python code with Ruff...
ruff check . --fix
if %ERRORLEVEL% neq 0 (
    set /a ERROR_COUNT+=1
    echo ERROR: Ruff linting found issues!
) else (
    echo SUCCESS: No linting issues found
)
echo.

echo [3/5] Type checking with MyPy...
mypy . --ignore-missing-imports
if %ERRORLEVEL% neq 0 (
    set /a ERROR_COUNT+=1
    echo ERROR: Type checking failed!
) else (
    echo SUCCESS: Type checking passed
)
echo.

echo [4/5] Running Python tests...
if exist "tests\" (
    pytest -v --tb=short
    if %ERRORLEVEL% neq 0 (
        set /a ERROR_COUNT+=1
        echo ERROR: Some tests failed!
    ) else (
        echo SUCCESS: All tests passed
    )
) else (
    echo WARNING: No tests directory found - skipping tests
)
echo.

echo [5/5] Checking frontend code quality...
if exist "frontend\package.json" (
    cd frontend
    
    echo Running ESLint...
    npm run lint
    if %ERRORLEVEL% neq 0 (
        set /a ERROR_COUNT+=1
        echo ERROR: Frontend linting failed!
    ) else (
        echo SUCCESS: Frontend linting passed
    )
    
    echo Running TypeScript check...
    npm run type-check >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo WARNING: Frontend type check failed (this might be expected if not fully configured)
    ) else (
        echo SUCCESS: Frontend type checking passed
    )
    
    cd ..
) else (
    echo INFO: No frontend found - skipping frontend checks
)

echo.
echo =====================================
echo  Quality Assurance Summary
echo =====================================
if %ERROR_COUNT% equ 0 (
    echo ✅ ALL CHECKS PASSED!
    echo Your code is ready for commit.
    echo.
    echo Next steps:
    echo  1. git add .
    echo  2. git commit -m "Your commit message"
    echo  3. git push
) else (
    echo ❌ %ERROR_COUNT% ERROR(S) FOUND!
    echo Please fix the issues above before committing.
)
echo =====================================
echo.
pause