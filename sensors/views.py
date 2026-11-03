from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorReading
from .serializers import SensorReadingSerializer, TelemetryIngestSerializer

class IngestReadingAPIView(APIView):
    """
    Ingests sensor telemetry packets transmitted by the ESP32 bridge.
    Endpoint: POST /api/sensors/readings/
    """
    def post(self, request):
        # Validate Station Secret Key
        secret = request.headers.get('X-Station-Secret') or request.data.get('secret')
        expected_secret = getattr(settings, 'STATION_API_SECRET', 'weather-station-secret-key-2026')
        if secret and secret != expected_secret:
            return Response({"error": "Unauthorized sensor node"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TelemetryIngestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        ts = timezone.now()
        if 'gateway_ts' in data and data['gateway_ts']:
            try:
                ts = datetime.fromtimestamp(data['gateway_ts'], tz=timezone.get_current_timezone())
            except Exception:
                ts = timezone.now()

        reading = SensorReading(
            station_id=data.get('station_id', 'chennai_station_01'),
            timestamp=ts,
            bmp_temp=data['bmp_temp'],
            bmp_pressure=data['bmp_pressure'],
            bmp_altitude=data.get('bmp_altitude', 0.0),
            bmp_ok=bool(data.get('bmp_ok', 1)),
            sht_temp=data['sht_temp'],
            sht_humidity=data['sht_humidity'],
            sht_ok=bool(data.get('sht_ok', 1)),
            rssi=data.get('rssi', 0),
        )
        reading.save()

        # Check for hazard patterns and trigger alerts
        alert_triggered = False
        try:
            from alerts.services import evaluate_telemetry_for_hazards
            alert_triggered = evaluate_telemetry_for_hazards(reading)
        except Exception as e:
            # Don't let alert evaluation failure crash ingestion
            pass

        return Response({
            "status": "success",
            "reading_id": reading.id,
            "timestamp": reading.timestamp.isoformat(),
            "fused_temp": reading.fused_temp,
            "dew_point": reading.dew_point,
            "heat_index": reading.heat_index,
            "pressure_trend_3h": reading.pressure_trend_3h,
            "alert_triggered": alert_triggered
        }, status=status.HTTP_201_CREATED)

class LatestReadingAPIView(APIView):
    """
    Returns the most recent reading from the local weather station.
    Endpoint: GET /api/sensors/latest/
    """
    def get(self, request):
        latest = SensorReading.objects.order_by('-timestamp').first()
        if not latest:
            return Response({"message": "No sensor readings recorded yet."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SensorReadingSerializer(latest)
        return Response(serializer.data)

class LiveHardwareStatusAPIView(APIView):
    """
    Returns real-time connection status of the ESP32/Arduino hardware station,
    including heartbeat latency, packet counts, and recent raw telemetry feed.
    Endpoint: GET /api/sensors/hardware-status/
    """
    def get(self, request):
        now = timezone.now()
        latest = SensorReading.objects.order_by('-timestamp').first()

        # Determine if hardware is currently transmitting (packet within last 180 seconds)
        is_connected = False
        seconds_ago = None
        if latest:
            diff = (now - latest.timestamp).total_seconds()
            seconds_ago = max(0, int(diff))
            if seconds_ago <= 180:
                is_connected = True

        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        packets_today = SensorReading.objects.filter(timestamp__gte=today_start).count()
        total_packets = SensorReading.objects.count()

        # Fetch the 12 most recent raw packets for the live ingestion terminal
        recent_qs = SensorReading.objects.order_by('-timestamp')[:12]
        recent_packets = []
        for r in recent_qs:
            recent_packets.append({
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "station_id": r.station_id,
                "bmp_temp": r.bmp_temp,
                "bmp_pressure": r.bmp_pressure,
                "bmp_ok": r.bmp_ok,
                "dht_temp": r.sht_temp, # Mapped from DHT11
                "dht_humidity": r.sht_humidity,
                "dht_ok": r.sht_ok,
                "fused_temp": r.fused_temp,
                "dew_point": r.dew_point,
                "heat_index": r.heat_index,
                "pressure_trend_3h": r.pressure_trend_3h,
                "rssi": r.rssi
            })

        return Response({
            "is_connected": is_connected,
            "seconds_since_last_packet": seconds_ago,
            "last_packet_time": latest.timestamp.isoformat() if latest else None,
            "packets_today": packets_today,
            "total_packets": total_packets,
            "latest_reading": SensorReadingSerializer(latest).data if latest else None,
            "recent_packets": recent_packets,
            "station_config": {
                "station_id": getattr(settings, 'STATION_NAME', 'Poonamallee Weather Observatory'),
                "latitude": getattr(settings, 'STATION_LATITUDE', 13.089017),
                "longitude": getattr(settings, 'STATION_LONGITUDE', 80.102193),
                "ingest_endpoint": "/api/sensors/readings/",
                "auth_header": "X-Station-Secret: weather-station-secret-key-2026"
            }
        })

class HistoricalReadingsAPIView(APIView):
    """
    Returns historical readings filtered by range (e.g. 24h, 7d, 30d).
    Endpoint: GET /api/sensors/history/?range=24h
    """
    def get(self, request):
        range_param = request.query_params.get('range', '24h')
        now = timezone.now()

        if range_param == '7d':
            start_time = now - timedelta(days=7)
            stride = 6 # Downsample roughly every 6th reading (~6 min)
        elif range_param == '30d':
            start_time = now - timedelta(days=30)
            stride = 30 # Downsample
        else: # 24h default
            start_time = now - timedelta(hours=24)
            stride = 1

        qs = SensorReading.objects.filter(timestamp__gte=start_time).order_by('timestamp')
        readings = list(qs)

        # Downsample if list is large to maintain lightning-fast frontend responsiveness
        if stride > 1 and len(readings) > 300:
            readings = readings[::stride]

        serializer = SensorReadingSerializer(readings, many=True)
        return Response({
            "range": range_param,
            "count": len(readings),
            "readings": serializer.data
        })
