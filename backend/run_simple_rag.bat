@echo off
echo ========================================
echo   GREEN UNIVERSITY SIMPLE RAG SERVER
echo ========================================
echo.
echo This server uses:
echo   - Dataset-first approach
echo   - Exact answer matching
echo   - Terminal reference logging
echo   - No unnecessary LLM generation
echo.
echo Starting server...
echo.
cd /d "%~dp0"
python simple_rag_server.py
pause
