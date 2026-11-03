from django.urls import path
from .views import IngestReadingAPIView, LatestReadingAPIView, HistoricalReadingsAPIView, LiveHardwareStatusAPIView

urlpatterns = [
    path('readings/', IngestReadingAPIView.as_view(), name='ingest-reading'),
    path('latest/', LatestReadingAPIView.as_view(), name='latest-reading'),
    path('history/', HistoricalReadingsAPIView.as_view(), name='historical-readings'),
    path('hardware-status/', LiveHardwareStatusAPIView.as_view(), name='hardware-status'),
]
