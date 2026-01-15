# HRMS Application Startup Script

Write-Host "Starting HRMS Application..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\env\Scripts\activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\env\Scripts\activate.ps1
} else {
    Write-Host "Virtual environment not found. Please create it first." -ForegroundColor Red
    exit
}

# Start Django server in background
Write-Host "Starting Django server on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\env\Scripts\activate.ps1; python manage.py runserver"

# Wait a bit for Django to start
Start-Sleep -Seconds 3

# Start React server
Write-Host "Starting React server on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm start"

Write-Host ""
Write-Host "✓ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "Django Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "React Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
