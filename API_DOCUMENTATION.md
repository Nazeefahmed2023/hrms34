# API Documentation - HRMS

Base URL: `http://localhost:8000/api`

## Authentication Endpoints

### Login
- **POST** `/accounts/login/`
- Body: `{ "username": "string", "password": "string" }`
- Response: `{ "message": "Login successful", "user": {...} }`

### Logout
- **POST** `/accounts/logout/`
- Requires: Authentication
- Response: `{ "message": "Logout successful" }`

### Get Current User
- **GET** `/accounts/current-user/`
- Requires: Authentication
- Response: User object with role

## Dashboard Endpoints

### Get Dashboard Data
- **GET** `/dashboard/`
- Requires: Authentication
- Response: Role-specific dashboard data

### Get Department Stats
- **GET** `/dashboard/stats/`
- Requires: Authentication
- Response: Array of department employee counts

## Employee Endpoints

### List Employees
- **GET** `/employees/list/`
- Requires: Admin/HR role
- Response: Array of employee objects

### Create Employee
- **POST** `/employees/create/`
- Requires: Admin/HR role
- Body:
```json
{
  "username": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "department": integer,
  "designation": integer,
  "date_of_joining": "YYYY-MM-DD",
  "basic_salary": "decimal"
}
```

### Get Employee Detail
- **GET** `/employees/detail/{id}/`
- Requires: Admin/HR role

### Update Employee
- **PUT** `/employees/detail/{id}/`
- Requires: Admin/HR role

### Delete Employee
- **DELETE** `/employees/detail/{id}/`
- Requires: Admin/HR role

### Get Departments
- **GET** `/employees/departments/`
- Requires: Authentication

### Get Designations
- **GET** `/employees/designations/`
- Requires: Authentication

### Update Department Manager
- **POST** `/employees/departments/update-manager/`
- Requires: Admin/HR role
- Body: `{ "department_id": integer, "manager_id": integer }`

### Get Employee Profile
- **GET** `/employees/profile/`
- Requires: Authentication
- Response: Current user's profile

### Update Employee Profile
- **PUT** `/employees/profile/`
- Requires: Authentication
- Body: Profile fields (multipart/form-data for file upload)

### View Any Profile
- **GET** `/employees/view-profile/?emp={employee_id}`
- Requires: Authentication + appropriate permissions

### Get Pending Profiles
- **GET** `/employees/pending-profiles/`
- Requires: Admin/HR role

### Approve Profile
- **POST** `/employees/approve-profile/{profile_id}/`
- Requires: Admin/HR role

## Attendance Endpoints

### Get Today's Attendance
- **GET** `/attendance/today/`
- Requires: Authentication
- Response: Current user's attendance for today

### Check In
- **POST** `/attendance/check-in/`
- Requires: Authentication
- Response: Updated attendance record

### Check Out
- **POST** `/attendance/check-out/`
- Requires: Authentication
- Response: Updated attendance record

### Get Monthly Attendance
- **GET** `/attendance/monthly/?month={1-12}&year={YYYY}`
- Requires: Authentication
- Response: Array of attendance records for the month

### Get Manager Team Attendance
- **GET** `/attendance/manager-team/`
- Requires: Manager role
- Response: Team attendance for today

## Leave Endpoints

### List Leaves
- **GET** `/leaves/list/`
- Requires: Authentication
- Response: User's leave requests (employee) or all leaves (admin/HR)

### Apply Leave
- **POST** `/leaves/apply/`
- Requires: Employee role
- Body:
```json
{
  "leave_type": "CL|SL|PL|LOP",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "reason": "string"
}
```

### Admin - List All Leaves
- **GET** `/leaves/admin/list/`
- Requires: Admin/HR role

### Admin - Approve Leave
- **POST** `/leaves/admin/approve/{id}/`
- Requires: Admin/HR role

### Admin - Reject Leave
- **POST** `/leaves/admin/reject/{id}/`
- Requires: Admin/HR role

### Manager - List Team Leaves
- **GET** `/leaves/manager/list/`
- Requires: Manager role

### Manager - Approve Leave
- **POST** `/leaves/manager/approve/{id}/`
- Requires: Manager role

### Manager - Reject Leave
- **POST** `/leaves/manager/reject/{id}/`
- Requires: Manager role

## Payroll Endpoints

### List Payroll
- **GET** `/payroll/list/?month={1-12}&year={YYYY}`
- Requires: Authentication
- Response: Payroll records (filtered by user if employee)

### Get Payroll Detail
- **GET** `/payroll/detail/{id}/`
- Requires: Authentication

### Generate Payroll
- **POST** `/payroll/generate/`
- Requires: Admin/HR role
- Body:
```json
{
  "employee_id": integer,
  "month": integer (1-12),
  "year": integer
}
```

### Get Employees for Payroll
- **GET** `/payroll/employees/`
- Requires: Admin/HR role
- Response: List of all employees

## Response Formats

### Success Response
```json
{
  "data": {...},
  "message": "Success message"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": "Additional error details"
}
```

## HTTP Status Codes

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not authorized for this action
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Authentication

All endpoints (except login) require authentication. The application uses session-based authentication with CSRF protection.

### CSRF Token
For POST/PUT/DELETE requests, include the CSRF token in the `X-CSRFToken` header. The token is automatically retrieved from cookies.

### Credentials
Set `withCredentials: true` in Axios to include cookies with requests.

## Permissions

- **ADMIN**: Full access to all endpoints
- **HR**: Access to employee, leave, and payroll management
- **MANAGER**: Access to team-related endpoints
- **EMPLOYEE**: Access to personal data and self-service features
