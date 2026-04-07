@echo off
REM Start Local Web Server for Dashboard
cd /d "%~dp0"
echo Starting local web server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python -m http.server 8000
pause
