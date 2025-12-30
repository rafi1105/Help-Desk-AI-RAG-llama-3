@echo off
echo ============================================
echo Starting GreenBot Application (V2 Chatbot)
echo ============================================
echo.

REM Start backend server
echo [1/2] Starting Backend Server (V2 Enhanced Chatbot)...
start cmd /k "cd /d d:\VS Code\thesis-bot\chatbot\backend && python rag_api_server.py"
timeout /t 3 /nobreak >nul

REM Start frontend development server
echo [2/2] Starting Frontend React Server...
start cmd /k "cd /d d:\VS Code\thesis-bot\chatbot\frontend-react && npm run dev"

echo.
echo ============================================
echo GreenBot is starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo ============================================
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill all related processes
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1

echo.
echo All servers stopped.
pause
