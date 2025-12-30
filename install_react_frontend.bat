@echo off
echo ============================================
echo GreenBot React Frontend Setup
echo ============================================
echo.

echo Installing dependencies...
cd frontend-react

echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js found!
echo.
echo Installing npm packages...
call npm install

if errorlevel 1 (
    echo.
    echo ERROR: npm install failed!
    echo Trying with --legacy-peer-deps...
    call npm install --legacy-peer-deps
)

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo Next steps:
echo 1. Start backend: cd backend ^&^& python rag_api_server.py
echo 2. Start frontend: cd frontend-react ^&^& npm run dev
echo 3. Or use: start_react_app.bat
echo.
pause
