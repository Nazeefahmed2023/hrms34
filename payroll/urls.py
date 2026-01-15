from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('', views.payroll_list, name='list'),
    path('generate/<int:emp_id>/', views.generate_payroll, name='generate'),
    path('<int:pk>/payslip/', views.payslip_pdf, name='payslip_pdf'),
]
