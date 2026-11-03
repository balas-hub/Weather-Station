from rest_framework import serializers
from .models import WeatherForecast

class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = [
            'id', 'target_datetime', 'forecast_type',
            'predicted_temp', 'predicted_humidity', 'predicted_pressure',
            'predicted_rainfall_mm', 'predicted_condition', 'confidence_score',
            'temp_lower_bound', 'temp_upper_bound',
            'pressure_lower_bound', 'pressure_upper_bound',
            'generated_at', 'model_version'
        ]
