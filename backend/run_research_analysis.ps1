# Research Analysis Launcher - PowerShell
# ========================================

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                  RESEARCH ANALYSIS - QUICK START" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "..\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "..\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "Warning: Virtual environment not found. Using system Python." -ForegroundColor Red
}

Write-Host ""
Write-Host "Select an option:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Run DEMO (Generate sample data and show capabilities)" -ForegroundColor White
Write-Host "2. Run FULL RESEARCH ANALYSIS (Analyze collected data)" -ForegroundColor White
Write-Host "3. Start SERVER with evaluation tracking" -ForegroundColor White
Write-Host "4. View API documentation" -ForegroundColor White
Write-Host "5. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Running evaluation demo..." -ForegroundColor Green
        python demo_evaluation.py
    }
    "2" {
        Write-Host ""
        Write-Host "Running full research analysis..." -ForegroundColor Green
        python research_analysis.py
    }
    "3" {
        Write-Host ""
        Write-Host "Starting server with evaluation tracking..." -ForegroundColor Green
        Write-Host "Server will be available at: http://localhost:5000" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "API Endpoints:" -ForegroundColor Cyan
        Write-Host "  GET  /analytics/live   - Live statistics" -ForegroundColor White
        Write-Host "  GET  /analytics/report - Full research report" -ForegroundColor White
        Write-Host "  GET  /analytics/export - Export to CSV" -ForegroundColor White
        Write-Host ""
        python simple_rag_server.py
    }
    "4" {
        Write-Host ""
        Write-Host "API DOCUMENTATION" -ForegroundColor Cyan
        Write-Host "=================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Base URL: http://localhost:5000" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Available Endpoints:" -ForegroundColor Green
        Write-Host "  POST /chat                - Send chat message" -ForegroundColor White
        Write-Host "  GET  /analytics/live      - Get live statistics" -ForegroundColor White
        Write-Host "  GET  /analytics/report    - Generate research report" -ForegroundColor White
        Write-Host "  GET  /analytics/export    - Export data to CSV" -ForegroundColor White
        Write-Host "  GET  /health              - Health check" -ForegroundColor White
        Write-Host "  GET  /stats               - Dataset statistics" -ForegroundColor White
        Write-Host "  POST /feedback            - Submit feedback" -ForegroundColor White
        Write-Host ""
        Write-Host "Example Usage:" -ForegroundColor Green
        Write-Host "  Invoke-WebRequest http://localhost:5000/analytics/live" -ForegroundColor Gray
        Write-Host "  Invoke-WebRequest http://localhost:5000/analytics/report" -ForegroundColor Gray
        Write-Host ""
    }
    "5" {
        Write-Host ""
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host ""
        Write-Host "Invalid choice. Please select 1-5." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
