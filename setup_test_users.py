"""
Setup test users for HRMS E2E testing
"""

from django.core.management.base import BaseCommand
from accounts.models import User
from employees.models import Employee, Department, Designation

def setup_test_users():
    """Create or update test users with known passwords"""
    
    # Create test admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@hrms.com',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True
        }
    )
    admin.set_password('admin123')
    admin.save()
    print(f"{'Created' if created else 'Updated'} admin user: admin/admin123")
    
    # Create test HR user
    hr_user, created = User.objects.get_or_create(
        username='hr',
        defaults={
            'email': 'hr@hrms.com',
            'role': 'HR'
        }
    )
    hr_user.set_password('hr123')
    hr_user.save()
    print(f"{'Created' if created else 'Updated'} HR user: hr/hr123")
    
    # Get or create department and designation
    dept, _ = Department.objects.get_or_create(
        name='Engineering'
    )
    
    designation, _ = Designation.objects.get_or_create(
        name='Software Engineer'
    )
    
    # Create test employee user
    emp_user, created = User.objects.get_or_create(
        username='employee',
        defaults={
            'email': 'employee@hrms.com',
            'role': 'EMPLOYEE',
            'first_name': 'Test',
            'last_name': 'Employee'
        }
    )
    emp_user.set_password('emp123')
    emp_user.save()
    
    # Create Employee record
    employee, emp_created = Employee.objects.get_or_create(
        user=emp_user,
        defaults={
            'employee_id': 'EMP001',
            'department': dept,
            'designation': designation,
            'date_of_joining': '2024-01-01',
            'basic_salary': 50000
        }
    )
    print(f"{'Created' if created else 'Updated'} employee user: employee/emp123")
    
    # Create manager user
    mgr_user, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'email': 'manager@hrms.com',
            'role': 'MANAGER',
            'first_name': 'Test',
            'last_name': 'Manager'
        }
    )
    mgr_user.set_password('mgr123')
    mgr_user.save()
    
    manager, mgr_emp_created = Employee.objects.get_or_create(
        user=mgr_user,
        defaults={
            'employee_id': 'MGR001',
            'department': dept,
            'designation': designation,
            'date_of_joining': '2023-01-01',
            'basic_salary': 80000
        }
    )
    print(f"{'Created' if created else 'Updated'} manager user: manager/mgr123")
    
    # Set manager for department
    if not dept.manager:
        dept.manager = manager
        dept.save()
        print(f"Set {manager.first_name} as manager of {dept.name}")
    
    print("\n✅ Test users setup complete!")
    print("\nTest Credentials:")
    print("  Admin:    admin/admin123")
    print("  HR:       hr/hr123")
    print("  Manager:  manager/mgr123")
    print("  Employee: employee/emp123")

if __name__ == '__main__':
    import os
    import django
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
    django.setup()
    
    setup_test_users()
