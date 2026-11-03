from datetime import datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import predictor_ensemble
from .scheduler import run_nightly_retraining, regenerate_cached_24h_forecast
from forecasts.models import WeatherForecast
from forecasts.serializers import WeatherForecastSerializer

class ModelForecast24HourAPIView(APIView):
    """
    Returns the 24-hour hourly AI weather forecast.
    Endpoint: GET /api/ai/forecast-24h/
    """
    def get(self, request):
        now = timezone.now()
        # Check if we have valid forecasts generated recently (within 4 hours)
        recent_forecasts = WeatherForecast.objects.filter(
            forecast_type='24h_hourly',
            target_datetime__gte=now
        ).order_by('target_datetime')

        if recent_forecasts.count() < 12:
            # Generate new forecast on demand
            try:
                regenerate_cached_24h_forecast()
                recent_forecasts = WeatherForecast.objects.filter(
                    forecast_type='24h_hourly',
                    target_datetime__gte=now
                ).order_by('target_datetime')
            except Exception as e:
                return Response({"error": f"Failed to generate forecast: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = WeatherForecastSerializer(recent_forecasts, many=True)
        return Response({
            "status": "success",
            "model_version": predictor_ensemble.version,
            "count": len(serializer.data),
            "forecasts": serializer.data
        })

class PredictFutureDateAPIView(APIView):
    """
    Predicts weather for an arbitrary date in the future (tomorrow, next month, or years ahead).
    Endpoint: GET /api/ai/predict-date/?date=YYYY-MM-DD
    """
    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Query parameter 'date' (YYYY-MM-DD) is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Expected YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        projection = predictor_ensemble.predict_future_date(target_date)
        return Response({
            "status": "success",
            "model_version": predictor_ensemble.version,
            "projection": projection
        })

class TriggerRetrainAPIView(APIView):
    """
    Triggers immediate model retraining and returns metrics.
    Endpoint: POST /api/ai/retrain/
    """
    def post(self, request):
        try:
            run_nightly_retraining()
            return Response({
                "status": "retrained",
                "message": "AI Ensemble retrained successfully with latest sensor and historical data.",
                "metrics": predictor_ensemble.metrics
            })
        except Exception as e:
            return Response({"error": f"Retraining failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ModelStatusAPIView(APIView):
    """
    Returns AI model version and performance evaluation metrics.
    Endpoint: GET /api/ai/status/
    """
    def get(self, request):
        return Response({
            "model_version": predictor_ensemble.version,
            "is_trained": predictor_ensemble.is_trained,
            "metrics": predictor_ensemble.metrics,
            "station": "Poonamallee Weather Station AI",
            "coordinates": {"latitude": 13.089017, "longitude": 80.102193}
        })
