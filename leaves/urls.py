from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    # Employee
    path('', views.leave_list, name='list'),
    path('apply/', views.apply_leave, name='apply'),

    # Admin / HR
    path('manage/', views.admin_leave_list, name='admin_list'),
    path('<int:pk>/approve/', views.approve_leave, name='approve'),
    path('<int:pk>/reject/', views.reject_leave, name='reject'),

    # Manager
    path('manager/', views.manager_leave_list, name='manager_list'),
    path('manager/<int:pk>/approve/', views.manager_approve_leave, name='manager_approve'),
    path('manager/<int:pk>/reject/', views.manager_reject_leave, name='manager_reject'),
    
]
