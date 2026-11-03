from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WeatherForecast
from .serializers import WeatherForecastSerializer

class LatestForecastAPIView(APIView):
    """
    Returns the latest 24h forecast series.
    Endpoint: GET /api/forecasts/latest/
    """
    def get(self, request):
        forecasts = WeatherForecast.objects.filter(forecast_type='24h_hourly').order_by('target_datetime')[:24]
        serializer = WeatherForecastSerializer(forecasts, many=True)
        return Response({
            "count": len(serializer.data),
            "forecasts": serializer.data
        })
