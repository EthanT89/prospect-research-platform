@echo off
title API Testing Suite

echo =====================================
echo  API Testing Suite
echo =====================================
echo.

REM Check if curl is available
curl --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo curl not found. Trying PowerShell method...
    set USE_POWERSHELL=1
) else (
    set USE_POWERSHELL=0
)

echo Testing API endpoints...
echo.

REM Test 1: Health Check
echo [1/4] Testing health endpoint...
if %USE_POWERSHELL% equ 1 (
    powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method Get; Write-Host '✅ Health check passed:'; $response | ConvertTo-Json -Depth 3 } catch { Write-Host '❌ Health check failed:' $_.Exception.Message }"
) else (
    curl -s http://localhost:8000/health
    if %ERRORLEVEL% equ 0 (
        echo ✅ Health check passed
    ) else (
        echo ❌ Health check failed
    )
)
echo.

REM Test 2: Root endpoint
echo [2/4] Testing root endpoint...
if %USE_POWERSHELL% equ 1 (
    powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/' -Method Get; Write-Host '✅ Root endpoint passed:'; $response | ConvertTo-Json -Depth 3 } catch { Write-Host '❌ Root endpoint failed:' $_.Exception.Message }"
) else (
    curl -s http://localhost:8000/
    if %ERRORLEVEL% equ 0 (
        echo ✅ Root endpoint passed
    ) else (
        echo ❌ Root endpoint failed
    )
)
echo.

REM Test 3: Company Research (will likely fail without Supabase)
echo [3/4] Testing company research endpoint...
echo This test may fail if Supabase is not configured...
if %USE_POWERSHELL% equ 1 (
    powershell -Command "try { $body = @{ company_name = 'Test Company'; domain = 'test.com' } | ConvertTo-Json; $response = Invoke-RestMethod -Uri 'http://localhost:8000/research/company' -Method Post -Body $body -ContentType 'application/json'; Write-Host '✅ Company research passed:'; $response | ConvertTo-Json -Depth 3 } catch { Write-Host '⚠️  Company research failed (expected if Supabase not configured):' $_.Exception.Message }"
) else (
    curl -s -X POST http://localhost:8000/research/company -H "Content-Type: application/json" -d "{\"company_name\": \"Test Company\", \"domain\": \"test.com\"}"
    if %ERRORLEVEL% equ 0 (
        echo ✅ Company research endpoint responded
    ) else (
        echo ⚠️ Company research failed (expected if Supabase not configured)
    )
)
echo.

REM Test 4: API Documentation
echo [4/4] Testing API documentation...
if %USE_POWERSHELL% equ 1 (
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/docs' -Method Get; if ($response.StatusCode -eq 200) { Write-Host '✅ API documentation accessible' } else { Write-Host '❌ API documentation failed' } } catch { Write-Host '❌ API documentation failed:' $_.Exception.Message }"
) else (
    curl -s -I http://localhost:8000/docs | findstr "200 OK" >nul
    if %ERRORLEVEL% equ 0 (
        echo ✅ API documentation accessible
    ) else (
        echo ❌ API documentation failed
    )
)
echo.

echo =====================================
echo  API Testing Complete
echo =====================================
echo.
echo Available endpoints:
echo  - Health: http://localhost:8000/health
echo  - Root: http://localhost:8000/  
echo  - Company Research: http://localhost:8000/research/company
echo  - API Docs: http://localhost:8000/docs
echo  - Companies List: http://localhost:8000/companies
echo.
echo If any tests failed, ensure:
echo  1. API server is running (run dev-start.bat)
echo  2. Virtual environment is activated
echo  3. Supabase configuration is complete (.env file)
echo =====================================
echo.
pause