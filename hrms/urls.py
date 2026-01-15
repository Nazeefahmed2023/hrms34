"""
URL configuration for hrms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .views import ReactAppView

def home(request):
    # Show welcome page instead of redirecting directly to login
    from django.shortcuts import render
    return render(request, 'welcome.html')

urlpatterns = [
    path('', home),                                 # "/" → login page
    path('accounts/', include('accounts.urls')),    # login, logout
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('leaves/', include('leaves.urls')),
    path('payroll/', include('payroll.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reports/', include('reports.urls')),
    
    # API URLs
    path('api/accounts/', include('accounts.api_urls')),
    path('api/employees/', include('employees.api_urls')),
    path('api/attendance/', include('attendance.api_urls')),
    path('api/leaves/', include('leaves.api_urls')),
    path('api/payroll/', include('payroll.api_urls')),
    path('api/dashboard/', include('dashboard.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)

# Catch-all pattern to serve React app (must be last)
# This allows React Router to handle frontend routes
urlpatterns += [
    re_path(r'^react/.*$', ReactAppView.as_view(), name='react_app'),
]

