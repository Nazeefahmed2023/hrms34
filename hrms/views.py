from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import os

class ReactAppView(TemplateView):
    """
    Serves the React application
    """
    def get(self, request, *args, **kwargs):
        try:
            # Serve the React index.html from the build folder
            return render(request, 'index.html')
        except Exception as e:
            # If React build doesn't exist, show a helpful message
            return render(request, 'base.html', {
                'error': 'React build not found. Please run: cd frontend && npm run build'
            })
