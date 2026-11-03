from django.urls import path
from .views import LatestForecastAPIView

urlpatterns = [
    path('latest/', LatestForecastAPIView.as_view(), name='latest-forecast'),
]
