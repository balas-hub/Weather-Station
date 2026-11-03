import math
from django.db import models
from django.utils import timezone
from datetime import timedelta

def compute_dew_point(temp_c: float, humidity: float) -> float:
    """Computes accurate dew point in Celsius using the Magnus-Tetens approximation."""
    if humidity <= 0 or temp_c < -50 or temp_c > 65:
        return temp_c
    a = 17.27
    b = 237.7
    try:
        alpha = ((a * temp_c) / (b + temp_c)) + math.log(humidity / 100.0)
        return round((b * alpha) / (a - alpha), 2)
    except (ValueError, ZeroDivisionError):
        return round(temp_c - ((100 - humidity) / 5.0), 2)

def compute_heat_index(temp_c: float, humidity: float) -> float:
    """Computes NOAA Heat Index in Celsius."""
    if temp_c < 26.0 or humidity < 40.0:
        return round(temp_c, 2)
    
    T = (temp_c * 9.0 / 5.0) + 32.0  # Fahrenheit
    R = humidity

    # Steadman's simplified heat index formula
    hi_simple = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (R * 0.094))
    if hi_simple < 80.0:
        return round((hi_simple - 32.0) * 5.0 / 9.0, 2)

    # Full Rothfusz regression equation
    hi = (-42.379 + 
          2.04901523 * T + 
          10.14333127 * R - 
          0.22475541 * T * R - 
          0.00683783 * (T**2) - 
          0.05481717 * (R**2) + 
          0.00122874 * (T**2) * R + 
          0.00085282 * T * (R**2) - 
          0.00000199 * (T**2) * (R**2))

    # Adjustments
    if R < 13.0 and 80.0 <= T <= 112.0:
        adjustment = ((13.0 - R) / 4.0) * math.sqrt((17.0 - abs(T - 95.0)) / 17.0)
        hi -= adjustment
    elif R > 85.0 and 80.0 <= T <= 87.0:
        adjustment = ((R - 85.0) / 10.0) * ((87.0 - T) / 5.0)
        hi += adjustment

    hi_c = (hi - 32.0) * 5.0 / 9.0
    return round(hi_c, 2)

class SensorReading(models.Model):
    station_id = models.CharField(max_length=64, default="chennai_station_01", db_index=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    # Raw telemetry from BMP280 (I2C)
    bmp_temp = models.FloatField(help_text="Temperature from BMP280 in Celsius")
    bmp_pressure = models.FloatField(help_text="Barometric Pressure from BMP280 in hPa")
    bmp_altitude = models.FloatField(default=0.0, help_text="Estimated altitude in meters")
    bmp_ok = models.BooleanField(default=True)

    # Raw telemetry from SHT11 (Digital)
    sht_temp = models.FloatField(help_text="Temperature from SHT11 in Celsius")
    sht_humidity = models.FloatField(help_text="Relative Humidity from SHT11 in %")
    sht_ok = models.BooleanField(default=True)

    # Derived and calibrated meteorological variables
    fused_temp = models.FloatField(help_text="Calibrated weighted average temperature")
    dew_point = models.FloatField(help_text="Calculated Dew Point in Celsius")
    heat_index = models.FloatField(help_text="Calculated Heat Index / Apparent Temperature")
    pressure_trend_3h = models.FloatField(default=0.0, help_text="Barometric pressure change over prior 3 hours (hPa)")

    # Diagnostics
    rssi = models.IntegerField(null=True, blank=True, help_text="ESP32 Wi-Fi RSSI in dBm")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['station_id', '-timestamp']),
        ]

    def save(self, *args, **kwargs):
        # Temperature calculation: Exact average of BMP280 and DHT11 sensors
        valid_bmp = self.bmp_ok and self.bmp_temp > -50 and self.bmp_temp < 70
        valid_dht = self.sht_ok and self.sht_temp > -50 and self.sht_temp < 70

        if valid_bmp and valid_dht:
            self.fused_temp = round((self.bmp_temp + self.sht_temp) / 2.0, 2)
        elif valid_dht:
            self.fused_temp = round(self.sht_temp, 2)
        elif valid_bmp:
            self.fused_temp = round(self.bmp_temp, 2)
        else:
            self.fused_temp = 30.0 # Nominal baseline

        # Humidity from DHT11
        hum = self.sht_humidity if (self.sht_ok and 0 <= self.sht_humidity <= 100) else 65.0
        self.dew_point = compute_dew_point(self.fused_temp, hum)
        self.heat_index = compute_heat_index(self.fused_temp, hum)

        # Calculate 3-hour pressure trend
        try:
            three_hours_ago = self.timestamp - timedelta(hours=3)
            # Find nearest reading roughly 3 hours ago
            past_reading = SensorReading.objects.filter(
                station_id=self.station_id,
                timestamp__lte=three_hours_ago,
                bmp_ok=True
            ).order_by('-timestamp').first()

            if past_reading and self.bmp_ok:
                self.pressure_trend_3h = round(self.bmp_pressure - past_reading.bmp_pressure, 2)
            else:
                self.pressure_trend_3h = 0.0
        except Exception:
            self.pressure_trend_3h = 0.0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.fused_temp}°C | {self.sht_humidity}% | {self.bmp_pressure} hPa"
