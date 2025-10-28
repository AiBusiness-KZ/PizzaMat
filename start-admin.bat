@echo off
echo ========================================
echo PizzaMat Admin Panel - Starting
echo ========================================
echo.

cd frontend

echo Starting development server...
echo.
echo Admin Panel will be available at:
echo http://localhost:5173/admin
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev
