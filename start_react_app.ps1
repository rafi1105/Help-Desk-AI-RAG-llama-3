# Start GreenBot Application (React + Vite version)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Starting GreenBot Application" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Start backend server
Write-Host "[1/2] Starting Backend Server..." -ForegroundColor Yellow
$backend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python rag_api_server.py" -PassThru
Start-Sleep -Seconds 3

# Start frontend development server
Write-Host "[2/2] Starting Frontend React Server..." -ForegroundColor Yellow
$frontend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend-react; npm run dev" -PassThru

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "GreenBot is starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers..." -ForegroundColor Yellow

# Wait for user to press Ctrl+C
try {
    Wait-Event -Timeout ([int]::MaxValue)
}
catch {
    # User pressed Ctrl+C
}
finally {
    Write-Host ""
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    
    # Stop processes
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue
    
    Write-Host "All servers stopped." -ForegroundColor Green
}
