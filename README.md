# HRMS with React Frontend

This is a complete Human Resource Management System (HRMS) with Django backend and React frontend.

## Features

### Role-Based Access:
- **Admin**: Manage employees, departments, leaves, payroll
- **HR**: Manage employees, approve profiles, manage leaves and payroll
- **Manager**: View team attendance, manage team leaves
- **Employee**: Mark attendance, apply for leaves, view profile

### Modules:
1. **Employee Management**: Create, edit, delete employees, manage departments
2. **Attendance**: Check-in/Check-out system with monthly reports
3. **Leave Management**: Apply leaves, approve/reject leaves
4. **Payroll**: Generate payroll with automatic calculations
5. **Profile Management**: Employee profiles with HR approval workflow

## Installation & Setup

### Backend (Django)

1. Navigate to project directory:
```bash
cd c:\Users\DELL\hrms34
```

2. Activate virtual environment:
```bash
.\env\Scripts\activate
```

3. Install dependencies (if not already installed):
```bash
pip install django-cors-headers
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser (if needed):
```bash
python manage.py createsuperuser
```

6. Start Django server:
```bash
python manage.py runserver
```

### Frontend (React)

1. Open a new terminal and navigate to frontend:
```bash
cd c:\Users\DELL\hrms34\frontend
```

2. Start React development server:
```bash
npm start
```

The React app will start on `http://localhost:3000`

## Usage

1. Access the application at `http://localhost:3000`
2. Login with your credentials
3. You'll be redirected to the appropriate dashboard based on your role

## Default Login

After creating a superuser via Django admin, you can:
- Access Django Admin: `http://localhost:8000/admin`
- Create users with different roles (ADMIN, HR, MANAGER, EMPLOYEE)

## API Endpoints

All API endpoints are available at `http://localhost:8000/api/`:

- `/api/accounts/` - Authentication endpoints
- `/api/employees/` - Employee management
- `/api/attendance/` - Attendance tracking
- `/api/leaves/` - Leave management
- `/api/payroll/` - Payroll operations
- `/api/dashboard/` - Dashboard data

## Tech Stack

### Backend:
- Django 5.1.6
- Django REST Framework
- SQLite Database
- django-cors-headers

### Frontend:
- React 19
- Material-UI (MUI)
- React Router
- Axios

## Project Structure

```
hrms34/
├── backend (Django apps)
│   ├── accounts/
│   ├── employees/
│   ├── attendance/
│   ├── leaves/
│   ├── payroll/
│   ├── dashboard/
│   └── reports/
└── frontend/ (React app)
    └── src/
        ├── components/
        ├── services/
        └── context/
```

## Notes

- The application uses session-based authentication with CSRF protection
- CORS is configured to allow requests from `http://localhost:3000`
- File uploads (employee photos) are stored in the `media/employee_photos/` directory
- Both servers must be running for the application to work properly
