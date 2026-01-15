from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Employee

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee_profile(sender, instance, created, **kwargs):
    """
    Auto-create Employee profile ONLY when a USER is created with role=EMPLOYEE
    and generate employee_id (E0001, E0002, ...)
    """
    if not created:
        return

    if instance.role != "EMPLOYEE":
        return

    # Create employee record
    emp = Employee.objects.create(
        user=instance,
        date_of_joining="2000-01-01",
        basic_salary=0
    )

    # Generate employee ID automatically
    emp.employee_id = f"E{emp.id:04d}"
    emp.save()
