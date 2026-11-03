from django.db import models
from django.utils import timezone

class WeatherForecast(models.Model):
    FORECAST_TYPES = [
        ('24h_hourly', '24-Hour Hourly Forecast'),
        ('multi_day', 'Multi-Day Forecast'),
        ('long_range', 'Long-Range Climate Projection'),
    ]

    CONDITION_CHOICES = [
        ('Clear / Sunny', 'Clear / Sunny'),
        ('Partly Cloudy', 'Partly Cloudy'),
        ('Overcast', 'Overcast'),
        ('Light Rain', 'Light Rain'),
        ('Moderate Rain', 'Moderate Rain'),
        ('Heavy Rain / Downpour', 'Heavy Rain / Downpour'),
        ('Thunderstorm', 'Thunderstorm'),
        ('Severe Storm / Cyclone Warning', 'Severe Storm / Cyclone Warning'),
        ('Extreme Heatwave', 'Extreme Heatwave'),
    ]

    target_datetime = models.DateTimeField(db_index=True)
    forecast_type = models.CharField(max_length=32, choices=FORECAST_TYPES, default='24h_hourly')
    
    # Core predicted meteorology
    predicted_temp = models.FloatField(help_text="Predicted temperature (°C)")
    predicted_humidity = models.FloatField(help_text="Predicted relative humidity (%)")
    predicted_pressure = models.FloatField(help_text="Predicted barometric pressure (hPa)")
    predicted_rainfall_mm = models.FloatField(default=0.0, help_text="Estimated precipitation (mm)")
    
    predicted_condition = models.CharField(max_length=64, choices=CONDITION_CHOICES, default='Clear / Sunny')
    confidence_score = models.FloatField(default=0.88, help_text="AI confidence score 0.0 - 1.0")

    # Quantile bounds / Prediction intervals (e.g. 10th and 90th percentile)
    temp_lower_bound = models.FloatField()
    temp_upper_bound = models.FloatField()
    pressure_lower_bound = models.FloatField()
    pressure_upper_bound = models.FloatField()

    # Meta
    generated_at = models.DateTimeField(default=timezone.now)
    model_version = models.CharField(max_length=64, default="tft_ensemble_v1.0")

    class Meta:
        ordering = ['target_datetime']
        indexes = [
            models.Index(fields=['forecast_type', 'target_datetime']),
        ]

    def __str__(self):
        return f"[{self.target_datetime:%Y-%m-%d %H:%M}] {self.predicted_condition} ({self.predicted_temp}°C, {self.confidence_score*100:.0f}%)"

class HistoricalWeatherRecord(models.Model):
    """
    Stores local and Open-Meteo ERA5 bootstrap historical weather data for Poonamallee, Chennai.
    Used for instant model retraining and pattern search.
    """
    timestamp = models.DateTimeField(unique=True, db_index=True)
    temperature_2m = models.FloatField()
    relative_humidity_2m = models.FloatField()
    surface_pressure = models.FloatField()
    precipitation = models.FloatField(default=0.0)
    wind_speed_10m = models.FloatField(default=0.0)
    cloud_cover = models.FloatField(default=0.0)
    weather_code = models.IntegerField(default=0)
    is_sensor_sourced = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M}: {self.temperature_2m}°C, {self.surface_pressure}hPa"
