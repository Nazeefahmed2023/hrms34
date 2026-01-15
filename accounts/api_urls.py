from django.urls import path
from . import api_views

urlpatterns = [
    path('login/', api_views.login_api, name='api_login'),
    path('logout/', api_views.logout_api, name='api_logout'),
    path('current-user/', api_views.current_user, name='api_current_user'),
]
