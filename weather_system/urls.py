"""
URL Configuration for weather_system.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('api/sensors/', include('sensors.urls')),
    path('api/forecasts/', include('forecasts.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/ai/', include('ai_engine.urls')),
]
