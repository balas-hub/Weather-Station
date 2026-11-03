from django.db import models
from django.utils import timezone

class HistoricalExtremeEvent(models.Model):
    """
    Catalog of historic extreme weather events in Chennai/Tamil Nadu region
    with characteristic atmospheric signatures for pattern matching.
    """
    CATEGORY_CHOICES = [
        ('Flood', 'Severe Urban / River Flooding'),
        ('Cyclone', 'Tropical Cyclone / Severe Storm'),
        ('Deluge', 'Extreme Monsoonal Deluge'),
        ('Heatwave', 'Dangerous Heatwave / Thermal Stress'),
        ('Depression', 'Deep Coastal Depression'),
    ]

    name = models.CharField(max_length=200, help_text="e.g. 2015 Chennai Mega Floods")
    event_date = models.CharField(max_length=64, help_text="e.g. December 1-4, 2015")
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    synopsis = models.TextField()
    peak_rainfall_mm = models.FloatField(default=0.0, help_text="Peak 24h rainfall in mm")
    barometric_drop_3h = models.FloatField(default=0.0, help_text="Typical pressure drop rate in 3 hours (hPa)")
    peak_humidity_pct = models.FloatField(default=95.0)
    peak_heat_index = models.FloatField(default=35.0)

    # 12-hour or 24-hour normalized pressure/humidity trend vector for DTW pattern matching
    pressure_trend_signature = models.JSONField(
        default=list, 
        help_text="Normalized sequence of pressure drops [0.0, -1.2, -3.5, -6.8, -12.0, ...]"
    )
    safety_advisory = models.TextField(help_text="Standard emergency advisory for this hazard type")

    def __str__(self):
        return f"{self.name} ({self.category} - {self.event_date})"

class HazardAlert(models.Model):
    SEVERITY_LEVELS = [
        ('LOW', 'Low Advisory'),
        ('MEDIUM', 'Moderate Alert'),
        ('HIGH', 'High Warning'),
        ('CRITICAL', 'Emergency / Hazard Warning'),
    ]

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    hazard_type = models.CharField(max_length=64, help_text="e.g. Cyclone Approach, Flood Risk, Heat Stress")
    severity = models.CharField(max_length=16, choices=SEVERITY_LEVELS, default='MEDIUM')
    
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Triggering snapshot metrics
    trigger_temp = models.FloatField(null=True, blank=True)
    trigger_humidity = models.FloatField(null=True, blank=True)
    trigger_pressure = models.FloatField(null=True, blank=True)
    trigger_pressure_trend = models.FloatField(null=True, blank=True)

    # Matched historical event analog
    matched_event_name = models.CharField(max_length=255, null=True, blank=True)
    matched_event_date = models.CharField(max_length=64, null=True, blank=True)
    matched_event_impact = models.TextField(null=True, blank=True)
    pattern_similarity_pct = models.FloatField(default=0.0, help_text="Pattern similarity score 0-100%")

    # Notification tracking
    channels_dispatched = models.JSONField(default=list, help_text="e.g. ['browser', 'email', 'telegram', 'sms']")
    is_active = models.BooleanField(default=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.hazard_type} ({self.created_at:%Y-%m-%d %H:%M})"
