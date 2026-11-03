from django.urls import path
from .views import (
    ActiveAlertsAPIView, 
    AcknowledgeAlertAPIView, 
    ClearAllAlertsAPIView,
    HistoricalEventsCatalogAPIView, 
    SimulateAlertAPIView,
    TelegramConfigAPIView,
    TelegramTestAlertAPIView
)

urlpatterns = [
    path('active/', ActiveAlertsAPIView.as_view(), name='active-alerts'),
    path('<int:alert_id>/dismiss/', AcknowledgeAlertAPIView.as_view(), name='dismiss-alert'),
    path('clear/', ClearAllAlertsAPIView.as_view(), name='clear-all-alerts'),
    path('historical-catalog/', HistoricalEventsCatalogAPIView.as_view(), name='historical-catalog'),
    path('simulate/', SimulateAlertAPIView.as_view(), name='simulate-alert'),
    path('test/', SimulateAlertAPIView.as_view(), name='trigger-test-alert'), # Alias for backward compatibility
    path('telegram/', TelegramConfigAPIView.as_view(), name='telegram-config'),
    path('telegram/test/', TelegramTestAlertAPIView.as_view(), name='telegram-test'),
]
