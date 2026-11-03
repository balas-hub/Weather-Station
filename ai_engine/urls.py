from django.urls import path
from .views import (
    ModelForecast24HourAPIView,
    PredictFutureDateAPIView,
    TriggerRetrainAPIView,
    ModelStatusAPIView
)

urlpatterns = [
    path('forecast-24h/', ModelForecast24HourAPIView.as_view(), name='ai-forecast-24h'),
    path('predict-date/', PredictFutureDateAPIView.as_view(), name='ai-predict-date'),
    path('retrain/', TriggerRetrainAPIView.as_view(), name='ai-retrain'),
    path('status/', ModelStatusAPIView.as_view(), name='ai-status'),
]
