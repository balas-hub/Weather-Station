import os
import sys

# Force UTF-8 stdout on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_system.settings')
django.setup()

from datetime import datetime, timedelta
from django.utils import timezone
from alerts.services import seed_historical_events_if_empty
from ai_engine.bootstrap import sync_bootstrap_to_database, fetch_open_meteo_historical_data
from ai_engine.model import predictor_ensemble
from ai_engine.scheduler import regenerate_cached_24h_forecast
from sensors.models import SensorReading

def bootstrap_full_system():
    print("==================================================================")
    print("  [*] Initializing AI Weather Prediction & Forecasting System")
    print("  [*] Location: Poonamallee, Chennai (13.089 N, 80.102 E)")
    print("==================================================================")

    # 1. Seed Historical Disasters
    print("\n[Step 1/5] Seeding Chennai Extreme Disaster Benchmark Signatures...")
    seed_historical_events_if_empty()
    print("[+] Catalog populated (2015 Floods, 2016 Vardah, 2020 Nivar, 2023 Michaung, 2024 Heatwave)")

    # 2. Fetch/Prepare ERA5 Bootstrap Data
    print("\n[Step 2/5] Preparing ERA5 Historical Atmospheric Dataset...")
    df_historical = fetch_open_meteo_historical_data(start_year=2023)
    sync_bootstrap_to_database()
    print("[+] Historical atmospheric corpus prepared.")

    # 3. Create Seed Sensor Readings for the last 48 hours
    print("\n[Step 3/5] Seeding baseline sensor observations...")
    now = timezone.now()
    if SensorReading.objects.count() < 24:
        for i in range(48, 0, -1):
            ts = now - timedelta(hours=i)
            # Daily diurnal cycle for Chennai
            hour = ts.hour
            t = 28.0 + 4.5 * (1.0 if 11 <= hour <= 15 else (-0.5 if hour <= 6 else 0.2))
            h = 75.0 - 15.0 * (1.0 if 11 <= hour <= 15 else 0.0)
            p = 1009.5 + 1.2 * (1.0 if hour in [9, 10, 21, 22] else -0.8)

            r = SensorReading(
                station_id="chennai_station_01",
                timestamp=ts,
                bmp_temp=round(t - 0.2, 2),
                bmp_pressure=round(p, 2),
                bmp_altitude=22.1,
                bmp_ok=True,
                sht_temp=round(t + 0.3, 2),
                sht_humidity=round(h, 1),
                sht_ok=True,
                rssi=-62
            )
            r.save()
        print(f"[+] Seeded 48 hourly sensor telemetry readings.")
    else:
        print(f"[+] Station already has {SensorReading.objects.count()} sensor records.")

    # 4. Train AI Forecasting Ensemble
    print("\n[Step 4/5] Training Custom AI Ensemble (TFT + Quantile HistGradient)...")
    sensor_qs = SensorReading.objects.filter(bmp_ok=True, sht_ok=True).order_by('timestamp')
    sensor_df = None
    if sensor_qs.exists():
        import pandas as pd
        sensor_df = pd.DataFrame(list(sensor_qs.values('timestamp', 'fused_temp', 'sht_humidity', 'bmp_pressure')))

    predictor_ensemble.fit(df_historical=df_historical, df_sensors=sensor_df)
    print(f"[+] AI Model Trained! MAE Temp: {predictor_ensemble.metrics.get('temp_mae')} C | R2: {predictor_ensemble.metrics.get('temp_r2')}")

    # 5. Generate 24-Hour Forecast
    print("\n[Step 5/5] Generating 24-Hour Hourly Forecasts...")
    regenerate_cached_24h_forecast()
    print("[+] 24-Hour forecast generated with 10th-90th quantile uncertainty envelopes.")

    print("\n==================================================================")
    print("  [OK] All systems fully operational and ready!")
    print("==================================================================")

if __name__ == '__main__':
    bootstrap_full_system()
