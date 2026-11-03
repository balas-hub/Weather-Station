import json
from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from sensors.models import SensorReading
from alerts.models import HistoricalExtremeEvent, HazardAlert
from ai_engine.model import predictor_ensemble

class WeatherSystemComprehensiveTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure model is ready
        if not predictor_ensemble.is_trained:
            predictor_ensemble.fit()

    def test_01_sensor_telemetry_ingest(self):
        """Tests ingestion endpoint receiving simulated packet from ESP32 with 3-pin DHT11."""
        payload = {
            "station_id": "chennai_station_01",
            "bmp_temp": 32.4,
            "bmp_pressure": 1008.2,
            "bmp_altitude": 22.0,
            "bmp_ok": 1,
            "dht_temp": 32.6,
            "dht_humidity": 78.5,
            "dht_ok": 1,
            "gateway_ts": int(timezone.now().timestamp()),
            "rssi": -58
        }
        response = self.client.post(
            '/api/sensors/readings/',
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_STATION_SECRET='weather-station-secret-key-2026'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertAlmostEqual(data["fused_temp"], 32.51, places=1)
        self.assertTrue(data["heat_index"] >= 32.0)
        self.assertTrue(data["dew_point"] > 0)

    def test_02_sensor_latest_and_history(self):
        """Tests latest reading and history endpoints."""
        # Create a sample reading
        r = SensorReading.objects.create(
            station_id="chennai_station_01",
            timestamp=timezone.now(),
            bmp_temp=30.0,
            bmp_pressure=1010.0,
            bmp_ok=True,
            sht_temp=30.0,
            sht_humidity=65.0,
            sht_ok=True
        )
        # Test latest
        res_latest = self.client.get('/api/sensors/latest/')
        self.assertEqual(res_latest.status_code, 200)
        self.assertEqual(res_latest.json()["station_id"], "chennai_station_01")

        # Test history
        res_hist = self.client.get('/api/sensors/history/?range=24h')
        self.assertEqual(res_hist.status_code, 200)
        self.assertGreaterEqual(res_hist.json()["count"], 1)

    def test_03_ai_forecast_24h(self):
        """Tests 24-hour hourly AI prediction endpoint."""
        response = self.client.get('/api/ai/forecast-24h/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["count"], 12)
        
        first_step = data["forecasts"][0]
        self.assertIn("predicted_temp", first_step)
        self.assertIn("predicted_pressure", first_step)
        self.assertIn("temp_lower_bound", first_step)
        self.assertIn("temp_upper_bound", first_step)
        self.assertIn("predicted_condition", first_step)

    def test_04_ai_predict_future_date_multi_year(self):
        """Tests multi-year arbitrary future date prediction (e.g. year 2028)."""
        future_date = "2028-11-15" # Northeast monsoon date in 2028
        response = self.client.get(f'/api/ai/predict-date/?date={future_date}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
        proj = data["projection"]
        self.assertEqual(proj["target_date"], future_date)
        self.assertTrue(18.0 <= proj["predicted_temp"] <= 42.0)
        self.assertTrue(proj["rain_probability_pct"] > 0)
        self.assertIn("Northeast Monsoon", proj["climatological_context"])

    def test_05_extreme_hazard_detection_and_pattern_match(self):
        """Tests hazard evaluation and DTW pattern matching against 2015 Chennai floods."""
        res = self.client.post(
            '/api/alerts/test/',
            data=json.dumps({"scenario": "storm"}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "alert_created")
        self.assertIsNotNone(data["matched_event"])
        self.assertGreater(data["similarity_pct"], 50.0)

        # Check active alerts list
        res_active = self.client.get('/api/alerts/active/')
        self.assertEqual(res_active.status_code, 200)
        self.assertGreaterEqual(res_active.json()["count"], 1)

    def test_06_dashboard_view_renders(self):
        """Tests that the main dashboard HTML template loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Poonamallee Weather Station")
        self.assertContains(response, "Future Date AI Predictor")
