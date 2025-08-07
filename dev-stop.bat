@echo off
title Stop Development Environment

echo =====================================
echo  Stopping Development Environment
echo =====================================
echo.

echo Stopping Python/FastAPI processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping process %%a running on port 8000
    taskkill /PID %%a /F >nul 2>&1
)

echo Stopping Node.js/Next.js processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    echo Stopping process %%a running on port 3000  
    taskkill /PID %%a /F >nul 2>&1
)

REM Close specific command prompt windows
taskkill /FI "WindowTitle eq Backend API*" /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend Dev*" /F >nul 2>&1

echo.
echo Development environment stopped!
echo.
pause