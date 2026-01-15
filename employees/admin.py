from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Employee, Department, Designation, EmployeeProfile

User = get_user_model()   # this returns the actual User model

class EmployeeAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="EMPLOYEE")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(EmployeeProfile)
