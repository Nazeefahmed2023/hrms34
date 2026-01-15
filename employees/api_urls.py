from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.employee_list_api, name='api_employee_list'),
    path('create/', api_views.create_employee_api, name='api_create_employee'),
    path('detail/<int:pk>/', api_views.employee_detail_api, name='api_employee_detail'),
    path('departments/', api_views.departments_api, name='api_departments'),
    path('departments/update-manager/', api_views.update_department_manager_api, name='api_update_department_manager'),
    path('designations/', api_views.designations_api, name='api_designations'),
    path('profile/', api_views.employee_profile_api, name='api_employee_profile'),
    path('view-profile/', api_views.view_profile_api, name='api_view_profile'),
    path('pending-profiles/', api_views.pending_profiles_api, name='api_pending_profiles'),
    path('approve-profile/<int:profile_id>/', api_views.approve_profile_api, name='api_approve_profile'),
]
