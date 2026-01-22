from django.urls import path, include
from . import views
from .views import update_profile, view_profile

# 🔥 API views

app_name = "employees"

urlpatterns = [
    # ==================================================
    # 🧩 DJANGO TEMPLATE VIEWS (HTML PAGES)
    # ==================================================
    path("", views.employee_list, name="employee_list"),
    path("create/", views.create_employee, name="create"),
    path("departments/", views.manage_departments, name="manage_departments"),
    path("update-profile/", update_profile, name="update_profile"),
    path("profile/", view_profile, name="view_profile"),
    # HR approvals
    path("pending-profiles/", views.pending_profiles, name="pending_profiles"),
    path("approve-profile/<int:profile_id>/", views.approve_profile, name="approve_profile"),
    path("edit/<int:emp_id>/", views.edit_employee, name="update"),
    path("delete/<int:emp_id>/", views.delete_employee, name="delete"),
    # Payroll integration
    path("payroll/", include("payroll.urls")),
]