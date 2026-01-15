from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.dashboard_api, name='api_dashboard'),
    path('stats/', api_views.stats_api, name='api_stats'),
]
