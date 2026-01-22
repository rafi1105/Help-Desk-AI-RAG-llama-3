@echo off
echo ========================================
echo   GREEN UNIVERSITY SIMPLE RAG SERVER
echo ========================================
echo.
echo This server uses:
echo   - Dataset-first approach
echo   - Exact answer matching
echo   - Terminal reference logging
echo   - Research evaluation tracking
echo.

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "..\..\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\..\.venv\Scripts\activate.bat"
    echo.
) else (
    echo Warning: Virtual environment not found at .venv
    echo Using system Python...
    echo.
)

echo Starting server...
echo.
python simple_rag_server.py
pause
