from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.leave_list_api, name='api_leave_list'),
    path('apply/', api_views.apply_leave_api, name='api_apply_leave'),
    path('admin/list/', api_views.admin_leave_list_api, name='api_admin_leave_list'),
    path('admin/approve/<int:pk>/', api_views.approve_leave_api, name='api_approve_leave'),
    path('admin/reject/<int:pk>/', api_views.reject_leave_api, name='api_reject_leave'),
    path('manager/list/', api_views.manager_leave_list_api, name='api_manager_leave_list'),
    path('manager/approve/<int:pk>/', api_views.manager_approve_leave_api, name='api_manager_approve_leave'),
    path('manager/reject/<int:pk>/', api_views.manager_reject_leave_api, name='api_manager_reject_leave'),
]
