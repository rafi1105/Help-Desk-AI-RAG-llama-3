@echo off
echo ========================================
echo   GREEN UNIVERSITY CHATBOT - STARTUP
echo ========================================
echo.
echo Starting Backend Server (Port 5000)...
start "RAG Server" cmd /k "cd /d %~dp0backend && python simple_rag_server.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend (Port 5173)...
start "React Frontend" cmd /k "cd /d %~dp0frontend-react && npm run dev"

echo.
echo ========================================
echo   BOTH SERVERS STARTED!
echo ========================================
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to exit this window...
pause > nul
