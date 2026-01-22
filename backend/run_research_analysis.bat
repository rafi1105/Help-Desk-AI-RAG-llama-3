@echo off
REM Research Analysis Launcher
REM ===========================

echo.
echo ================================================================================
echo                  RESEARCH ANALYSIS - QUICK START
echo ================================================================================
echo.

REM Set Python executable path
set PYTHON_EXE=D:\VS Code\Help-Desk-AI-RAG-llama-3\.venv\Scripts\python.exe

REM Check if virtual environment Python exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Virtual environment Python not found at: %PYTHON_EXE%
    echo Please ensure virtual environment is set up correctly.
    pause
    exit /b 1
)

echo Using Python from virtual environment: %PYTHON_EXE%
echo.
echo Select an option:
echo.
echo 1. POPULATE REALISTIC DEMO DATA (Mixed quality - shows real metrics 60-80%%)
echo 2. POPULATE PERFECT DEMO DATA (All perfect matches - shows 100%% metrics)
echo 3. Run DEMO (Generate sample data and show capabilities)
echo 4. Run FULL RESEARCH ANALYSIS (Analyze collected data + Visualizations)
echo 5. Start SERVER with evaluation tracking
echo 6. Generate VISUALIZATIONS ONLY
echo 7. View API documentation
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo.
    echo Populating realistic demo data with varied answer quality...
    echo This creates answers with different quality levels (perfect, good, acceptable)
    echo Expected metrics: 60-80%% accuracy (realistic scenario)
    "%PYTHON_EXE%" populate_realistic_demo_data.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Populating perfect demo data (all answers match ground truth exactly)...
    echo Expected metrics: 100%% accuracy (ideal scenario)
    "%PYTHON_EXE%" populate_demo_data.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Populating perfect demo data (all answers match ground truth exactly)...
    echo Expected metrics: 100%% accuracy (ideal scenario)
    "%PYTHON_EXE%" populate_demo_data.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Running evaluation demo...
    "%PYTHON_EXE%" demo_evaluation.py
    goto end
)

if "%choice%"=="4" (
    echo.
    echo ================================================================================
    echo              RUNNING FULL RESEARCH ANALYSIS WITH VISUALIZATIONS
    echo ================================================================================
    echo.
    echo This will:
    echo   - Analyze all response logs and feedback data
    echo   - Calculate accuracy metrics (BLEU, Semantic Similarity, F1)
    echo   - Generate 10 publication-quality visualizations
    echo   - Create HTML report with interactive charts
    echo   - Export data to CSV for statistical analysis
    echo.
    echo Please wait...
    echo.
    "%PYTHON_EXE%" research_analysis.py
    echo.
    echo ================================================================================
    echo Press any key to return to menu...
    pause >nul
    goto end
)

if "%choice%"=="5" (
    echo.
    echo Starting server with evaluation tracking...
    echo Server will be available at: http://localhost:5000
    echo.
    echo API Endpoints:
    echo   GET  /analytics/live   - Live statistics
    echo   GET  /analytics/report - Full research report
    echo   GET  /analytics/export - Export to CSV
    echo.
    "%PYTHON_EXE%" simple_rag_server.py
    goto end
)

if "%choice%"=="6" (
    echo.
    echo Generating visualizations only...
    "%PYTHON_EXE%" research_visualization.py
    goto end
)

if "%choice%"=="7" (
    echo.
    echo API DOCUMENTATION
    echo ==================
    echo.
    echo Base URL: http://localhost:5000
    echo.
    echo Available Endpoints:
    echo   POST /chat                - Send chat message
    echo   GET  /analytics/live      - Get live statistics
    echo   GET  /analytics/report    - Generate research report
    echo   GET  /analytics/export    - Export data to CSV
    echo   GET  /health              - Health check
    echo   GET  /stats               - Dataset statistics
    echo   POST /feedback            - Submit feedback
    echo.
    echo Example Usage:
    echo   curl http://localhost:5000/analytics/live
    echo   curl http://localhost:5000/analytics/report
    echo.
    goto end
)

if "%choice%"=="8" (
    echo.
    echo Exiting...
    goto end
)

echo Invalid choice. Please select 1-8.

:end
echo.
echo Press any key to exit...
pause >nul
