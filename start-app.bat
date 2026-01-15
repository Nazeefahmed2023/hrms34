@echo off
echo Starting HRMS Application...
echo.

REM Start Django server in new window
echo Starting Django server on http://localhost:8000...
start "Django Server" cmd /k "cd /d %~dp0 && env\Scripts\activate && python manage.py runserver"

REM Wait a bit for Django to start
timeout /t 3 /nobreak > nul

REM Start React server in new window
echo Starting React server on http://localhost:3000...
start "React Server" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo Both servers are starting!
echo.
echo Django Backend: http://localhost:8000
echo React Frontend: http://localhost:3000
echo.
echo Close the command windows to stop the servers
pause
