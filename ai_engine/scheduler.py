import logging
import pandas as pd
from datetime import datetime, timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = None

def run_nightly_retraining():
    """
    Executes automated nightly retraining of the AI weather model at 02:00 AM IST.
    Pulls local sensor readings collected during the day, merges with historical baseline,
    and updates model weights and forecast tables.
    """
    print("[AI RETRAINER] Starting continuous daily retraining job...")
    try:
        from sensors.models import SensorReading
        from forecasts.models import HistoricalWeatherRecord, WeatherForecast
        from .model import predictor_ensemble
        from .bootstrap import fetch_open_meteo_historical_data

        # 1. Fetch local sensor readings
        sensors_qs = SensorReading.objects.filter(bmp_ok=True, sht_ok=True).order_by('timestamp')
        df_sensors = None
        if sensors_qs.count() > 10:
            sensor_data = list(sensors_qs.values('timestamp', 'fused_temp', 'sht_humidity', 'bmp_pressure'))
            df_sensors = pd.DataFrame(sensor_data)
            print(f"[AI RETRAINER] Ingested {len(df_sensors)} local sensor records for continuous learning.")

        # 2. Fetch baseline data
        df_historical = fetch_open_meteo_historical_data()

        # 3. Retrain ensemble
        predictor_ensemble.fit(df_historical=df_historical, df_sensors=df_sensors)

        # 4. Generate new 24-Hour forecast and update DB
        regenerate_cached_24h_forecast()

        print("[AI RETRAINER] Continuous model update completed successfully!")
    except Exception as e:
        print(f"[AI RETRAINER] Error during automated retraining: {e}")

def regenerate_cached_24h_forecast():
    """Regenerates 24-hour forecast records stored in SQLite."""
    from sensors.models import SensorReading
    from forecasts.models import WeatherForecast
    from .model import predictor_ensemble

    # Gather last 24-48 hours of sensor readings or synthesize reference state
    readings = list(SensorReading.objects.filter(bmp_ok=True, sht_ok=True).order_by('-timestamp')[:48])
    readings.reverse()

    if len(readings) >= 12:
        df_recent = pd.DataFrame([{
            'timestamp': pd.to_datetime(r.timestamp).tz_localize(None) if hasattr(r.timestamp, 'tzinfo') and r.timestamp.tzinfo else pd.to_datetime(r.timestamp),
            'temperature': r.fused_temp,
            'humidity': r.sht_humidity,
            'pressure': r.bmp_pressure,
            'precipitation': 0.0,
            'wind_speed': 5.0,
            'cloud_cover': 35.0,
            'weather_code': 1
        } for r in readings])
    else:
        # Construct reference context from current time
        now = timezone.now().replace(tzinfo=None)
        dates = pd.date_range(now - timedelta(hours=24), now, freq='1h')
        df_recent = pd.DataFrame({
            'timestamp': dates,
            'temperature': [31.5] * len(dates),
            'humidity': [72.0] * len(dates),
            'pressure': [1009.5] * len(dates),
            'precipitation': [0.0] * len(dates),
            'wind_speed': [5.0] * len(dates),
            'cloud_cover': [30.0] * len(dates),
            'weather_code': [1] * len(dates)
        })

    forecast_items = predictor_ensemble.predict_24h_hourly(df_recent)

    # Wipe obsolete forecasts and save fresh predictions
    WeatherForecast.objects.filter(forecast_type='24h_hourly').delete()
    db_items = []
    current_tz = timezone.get_current_timezone()
    for item in forecast_items:
        dt = datetime.fromisoformat(item['target_datetime'])
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, current_tz)

        db_items.append(WeatherForecast(
            target_datetime=dt,
            forecast_type='24h_hourly',
            predicted_temp=item['predicted_temp'],
            predicted_humidity=item['predicted_humidity'],
            predicted_pressure=item['predicted_pressure'],
            predicted_rainfall_mm=item['predicted_rainfall_mm'],
            predicted_condition=item['predicted_condition'],
            confidence_score=item['confidence_score'],
            temp_lower_bound=item['temp_lower_bound'],
            temp_upper_bound=item['temp_upper_bound'],
            pressure_lower_bound=item['pressure_lower_bound'],
            pressure_upper_bound=item['pressure_upper_bound'],
            generated_at=timezone.now(),
            model_version=predictor_ensemble.version
        ))
    WeatherForecast.objects.bulk_create(db_items)
    print(f"[AI RETRAINER] Saved {len(db_items)} hourly forecast intervals to SQLite.")

def start_weather_ai_scheduler():
    """Initializes APScheduler background daemon."""
    global scheduler
    if scheduler is not None and scheduler.running:
        return

    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    
    # Run nightly at 02:00 AM IST
    scheduler.add_job(
        run_nightly_retraining,
        trigger=CronTrigger(hour=2, minute=0, timezone="Asia/Kolkata"),
        id="nightly_model_retrain",
        name="Nightly Weather AI Retraining",
        replace_existing=True
    )

    scheduler.start()
    print("[AI SCHEDULER] Background scheduler active (Nightly auto-retrain registered for 02:00 AM IST).")
