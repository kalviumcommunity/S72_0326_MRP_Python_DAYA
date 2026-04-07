# Start Local Web Server for Dashboard
# Run this script to start the server and open dashboard in browser

Write-Host "🚀 Starting local web server..." -ForegroundColor Cyan
Write-Host "📍 URL: http://localhost:8000/dashboard.html" -ForegroundColor Green
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow

# Change to script directory
Set-Location $PSScriptRoot

# Start server
python -m http.server 8000
