from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.payroll_list_api, name='api_payroll_list'),
    path('detail/<int:pk>/', api_views.payroll_detail_api, name='api_payroll_detail'),
    path('generate/', api_views.generate_payroll_api, name='api_generate_payroll'),
    path('employees/', api_views.employees_for_payroll_api, name='api_employees_for_payroll'),
]
