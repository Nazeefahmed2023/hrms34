from django.urls import path
from . import api_views

urlpatterns = [
    path('today/', api_views.attendance_today_api, name='api_attendance_today'),
    path('check-in/', api_views.check_in_api, name='api_check_in'),
    path('check-out/', api_views.check_out_api, name='api_check_out'),
    path('monthly/', api_views.monthly_attendance_api, name='api_monthly_attendance'),
    path('manager-team/', api_views.manager_team_attendance_api, name='api_manager_team_attendance'),
]
