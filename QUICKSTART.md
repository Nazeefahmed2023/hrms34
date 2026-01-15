# Quick Start Guide - HRMS with React

## ⚡ Quick Setup (First Time)

### Step 1: Install Dependencies
```bash
# Activate virtual environment
.\env\Scripts\activate

# Install Django CORS package
pip install django-cors-headers

# Navigate to frontend and install packages (already done)
cd frontend
# npm install (already completed)
cd ..
```

### Step 2: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Admin User (if needed)
```bash
python manage.py createsuperuser
```

## 🚀 Starting the Application

### Option 1: Use the Startup Script (Easiest)
Double-click `start-app.bat` or run:
```bash
.\start-app.bat
```

### Option 2: Manual Start
Open two terminals:

**Terminal 1 - Django:**
```bash
.\env\Scripts\activate
python manage.py runserver
```

**Terminal 2 - React:**
```bash
cd frontend
npm start
```

## 📱 Accessing the Application

- **React Frontend**: http://localhost:3000
- **Django Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 👥 Creating Test Users

1. Go to Django Admin: http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to "Users" under "ACCOUNTS"
4. Click "Add User"
5. Set username, password, and select appropriate role:
   - ADMIN - Full system access
   - HR - Employee & leave management
   - MANAGER - Team management
   - EMPLOYEE - Personal attendance & leaves

## 📋 Testing the Application

### As ADMIN/HR:
1. Login at http://localhost:3000
2. Create employees via "Employees" → "Add Employee"
3. Manage departments and assign managers
4. Approve employee profiles
5. Manage leave requests
6. Generate payroll

### As MANAGER:
1. Login at http://localhost:3000
2. View team attendance dashboard
3. Approve/reject team leave requests
4. Monitor team presence

### As EMPLOYEE:
1. Login at http://localhost:3000
2. Mark attendance (Check-in/Check-out)
3. Update profile (requires HR approval)
4. Apply for leaves
5. View payslips

## 🔧 Troubleshooting

### CORS Errors:
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in settings.py includes `http://localhost:3000`

### 404 API Errors:
- Ensure Django server is running on port 8000
- Check that API URLs are correctly configured

### Login Issues:
- Check browser console for errors
- Verify CSRF token is being sent
- Ensure credentials are correct

### Port Already in Use:
- Django: Change port with `python manage.py runserver 8001`
- React: Will automatically prompt for different port

## 📁 Important Files

- `hrms/settings.py` - Django configuration
- `hrms/urls.py` - API routing
- `frontend/src/services/api.js` - API client
- `frontend/src/App.js` - React routing
- `frontend/src/context/AuthContext.js` - Authentication state

## 🎯 Key Features Implemented

✅ Role-based authentication and authorization
✅ Employee management (CRUD operations)
✅ Department and designation management
✅ Attendance tracking with check-in/check-out
✅ Leave application and approval workflow
✅ Payroll generation with automatic calculations
✅ Profile management with HR approval
✅ Responsive Material-UI design
✅ RESTful API architecture
✅ CSRF protection and CORS configuration

## 📞 Support

If you encounter any issues:
1. Check the browser console for errors
2. Check the Django server terminal for backend errors
3. Verify both servers are running
4. Check the README.md for detailed information
