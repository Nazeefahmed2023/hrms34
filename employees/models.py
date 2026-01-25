from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100)

    # 🔥 NEW: each department can have ONE manager (optional)
    manager = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managing_department'
    )

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username



from django.conf import settings

class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=50, blank=True, null=True)

    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)

    verified = models.BooleanField(default=False)   # 🔥 HR approval flag

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
