@echo off
echo ========================================
echo   HRMS First Time Setup
echo ========================================
echo.

echo [1/4] Installing Django dependencies...
call env\Scripts\activate
pip install django-cors-headers
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo [3/4] Creating media directories...
if not exist "media\employee_photos" mkdir media\employee_photos

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Create a superuser:
echo    python manage.py createsuperuser
echo.
echo 2. Start the application:
echo    start-app.bat
echo.
echo 3. Access admin panel:
echo    http://localhost:8000/admin
echo.
echo 4. Create test users with different roles
echo.
echo 5. Access the React app:
echo    http://localhost:3000
echo.
echo ========================================
pause
