from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_dashboard, name='dashboard'),
    path('employees/csv/', views.employees_csv, name='employees_csv'),
    path('employees/pdf/', views.employees_pdf, name='employees_pdf'),
    path("attendance/", views.attendance_report, name="attendance_report"),
    path("attendance/csv/", views.attendance_csv, name="attendance_csv"),
    path("attendance/pdf/", views.attendance_pdf, name="attendance_pdf"),
    path("payroll/", views.payroll_report, name="payroll_report"),
    path("payroll/pdf/", views.payroll_pdf, name="payroll_pdf"),


]
