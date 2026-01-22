from django.contrib.auth import get_user_model
from employees.models import Employee, EmployeeProfile, Department, Designation
from datetime import date

User = get_user_model()

# Create dummy department and designation if not exist
if not Department.objects.filter(name='DummyDept').exists():
    dept = Department.objects.create(name='DummyDept')
else:
    dept = Department.objects.get(name='DummyDept')

if not Designation.objects.filter(name='DummyDesig').exists():
    desig = Designation.objects.create(name='DummyDesig')
else:
    desig = Designation.objects.get(name='DummyDesig')

# Create dummy user
user, created = User.objects.get_or_create(username='pendinguser', defaults={
    'first_name': 'Pending',
    'last_name': 'User',
    'email': 'pendinguser@example.com',
})

# Create employee
employee, created = Employee.objects.get_or_create(user=user, defaults={
    'employee_id': 'EMP999',
    'department': dept,
    'designation': desig,
    'date_of_joining': date.today(),
    'basic_salary': 50000,
})

# Create pending profile
profile, created = EmployeeProfile.objects.get_or_create(employee=user, defaults={
    'phone': '1234567890',
    'personal_email': 'pendinguser@example.com',
    'address': '123 Dummy St',
    'verified': False,
})

print('Dummy pending profile created:', profile)
