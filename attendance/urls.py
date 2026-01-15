from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_page, name='page'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('monthly/', views.monthly, name='monthly'),
    path('team/', views.manager_team_attendance, name='manager_team'),
    
]
