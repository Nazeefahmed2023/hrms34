# HRMS - Quick Start Guide

## 🚀 System is Ready and Running!

Your HRMS (Human Resource Management System) is fully functional and ready to use.

---

## 🌐 Accessing the System

### Server is running at: **http://127.0.0.1:8000/**

### Two Ways to Use the System:

1. **Classic Django Interface** (Recommended for stability)
   - URL: http://127.0.0.1:8000/accounts/login/
   - Traditional server-rendered pages
   - Full feature set

2. **React Single Page Application**
   - URL: http://127.0.0.1:8000/react/
   - Modern UI with Material-UI
   - Fast and responsive

---

## 🔐 Login Credentials

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Admin** | admin | admin123 | Full system access |
| **HR** | hr | hr123 | HR operations |
| **Employee** | emp02 | emp123 | Employee self-service |

---

## ✨ Available Features

### For Admin Users:
✅ **Dashboard** - System overview and statistics
✅ **Employee Management** - Add, edit, view all employees
✅ **Department Management** - Manage departments and hierarchies
✅ **Leave Approvals** - Approve/reject leave requests
✅ **Payroll Processing** - Generate and manage payroll
✅ **Reports** - Generate various HR reports
✅ **User Management** - Create and manage user accounts

### For HR Users:
✅ **Employee Records** - Manage employee information
✅ **Leave Management** - Handle leave requests
✅ **Payroll Operations** - Process monthly payroll
✅ **Profile Verification** - Approve employee profiles
✅ **Department Operations** - Manage departments

### For Employees:
✅ **Personal Dashboard** - View personal information
✅ **Attendance** - Clock in/out, view attendance history
✅ **Apply for Leave** - Submit leave requests
✅ **View Payroll** - Check salary slips
✅ **Update Profile** - Manage personal information

---

## 📱 Main Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | http://127.0.0.1:8000/ | Welcome page with options |
| Login | http://127.0.0.1:8000/accounts/login/ | User login |
| Dashboard | http://127.0.0.1:8000/dashboard/ | Main dashboard |
| Employees | http://127.0.0.1:8000/employees/ | Employee management |
| Attendance | http://127.0.0.1:8000/attendance/ | Attendance tracking |
| Leaves | http://127.0.0.1:8000/leaves/ | Leave management |
| Payroll | http://127.0.0.1:8000/payroll/ | Payroll processing |
| Reports | http://127.0.0.1:8000/reports/ | Reports and analytics |

---

## 🔧 Common Tasks

### Starting the Server
```bash
cd c:\Users\DELL\hrms34
.\env\Scripts\activate
python manage.py runserver
```

### Stopping the Server
Press `CTRL+C` in the terminal, or:
```bash
Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process
```

### Creating New Users
```bash
python manage.py createsuperuser
```

### Accessing Admin Panel
URL: http://127.0.0.1:8000/admin/
Login with admin credentials

---

## 📊 System Status

✅ **Backend**: Django 6.0.1 - Running
✅ **Database**: SQLite - Connected
✅ **Frontend**: React 19.2.3 - Build Ready
✅ **APIs**: REST Framework - Active
✅ **Authentication**: Session-based - Working
✅ **CORS**: Configured - Enabled

**Total Users**: 9
**Total Employees**: 8
**Total Departments**: 4
**Leave Requests**: 3
**Payroll Records**: 14

---

## 💡 Tips for Usage

1. **First Time Login**: Use `admin / admin123` to access the system
2. **Navigation**: Use the top menu bar to navigate between modules
3. **Dashboard**: Provides quick overview of system status
4. **Role-Based**: Different users see different menus based on their role
5. **Real-time**: Most changes reflect immediately in the system

---

## 🔄 Workflow Examples

### Adding a New Employee
1. Login as Admin or HR
2. Go to Employees → Add Employee
3. Fill in employee details
4. Save - Employee account is created automatically

### Processing Attendance
1. Employee logs in
2. Go to Attendance
3. Click "Clock In" to mark attendance
4. Click "Clock Out" when leaving

### Applying for Leave
1. Employee logs in
2. Go to Leaves → Apply Leave
3. Select dates and leave type
4. Submit request
5. Admin/HR will approve or reject

### Generating Payroll
1. Admin/HR logs in
2. Go to Payroll → Generate
3. Select month and employees
4. System calculates automatically
5. Review and confirm

---

## 🎯 Next Steps

1. **Explore the Dashboard** - Get familiar with the interface
2. **Try Different Roles** - Login as different users to see role-based access
3. **Test Features** - Try creating employees, marking attendance, applying leaves
4. **Customize** - Add your organization's departments and designations
5. **Add Real Data** - Start adding actual employee information

---

## 🆘 Need Help?

- **Documentation**: Check `API_DOCUMENTATION.md` for API details
- **Setup Issues**: Review `QUICKSTART.md`
- **Conversion Notes**: See `CONVERSION_COMPLETE.md`

---

## ⚡ Quick Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Check migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

---

**System Status**: 🟢 **ONLINE AND READY**

**Last Updated**: January 15, 2026

Enjoy using your HRMS! 🎉
