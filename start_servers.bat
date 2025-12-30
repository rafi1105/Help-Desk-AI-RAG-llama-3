echo 🔧 Starting Backend Server...
start "Backend Server" cmd /k "cd /d d:\VS Code\thesis-bot\chatbot\backend && python rag_api_server.py"

timeout /t 3 /nobreak > nul

echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d d:\VS Code\thesis-bot\chatbot\frontend-react && npm run dev"

echo.
echo ✅ Servers started!
echo 📱 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:5000
echo.
echo Press any key to exit...
pause > nul
