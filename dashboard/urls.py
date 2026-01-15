from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stats-api/', views.stats_api, name='stats_api'),  # final + correct
]
