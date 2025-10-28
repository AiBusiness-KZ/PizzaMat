@echo off
echo ========================================
echo PizzaMat Admin Panel - Installation
echo ========================================
echo.

cd frontend

echo [1/3] Cleaning old dependencies...
if exist node_modules (
    rmdir /s /q node_modules
)
if exist package-lock.json (
    del package-lock.json
)

echo [2/3] Installing dependencies...
call npm install

if %errorlevel% neq 0 (
    echo.
    echo ERROR: npm install failed!
    echo Trying with --legacy-peer-deps...
    call npm install --legacy-peer-deps
)

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed!
    echo Please check if Node.js is installed correctly.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the admin panel, run:
echo   .\start-admin.bat
echo.
echo Or manually:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173/admin
echo.
pause
