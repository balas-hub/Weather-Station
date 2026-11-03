from rest_framework import serializers
from .models import SensorReading

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = [
            'id', 'station_id', 'timestamp',
            'bmp_temp', 'bmp_pressure', 'bmp_altitude', 'bmp_ok',
            'sht_temp', 'sht_humidity', 'sht_ok',
            'fused_temp', 'dew_point', 'heat_index', 'pressure_trend_3h',
            'rssi', 'created_at'
        ]
        read_only_fields = ['id', 'fused_temp', 'dew_point', 'heat_index', 'pressure_trend_3h', 'created_at']

class TelemetryIngestSerializer(serializers.Serializer):
    station_id = serializers.CharField(required=False, default="chennai_station_01")
    bmp_temp = serializers.FloatField(required=True)
    bmp_pressure = serializers.FloatField(required=True)
    bmp_altitude = serializers.FloatField(required=False, default=0.0)
    bmp_ok = serializers.IntegerField(required=False, default=1)
    
    # Supports both 3-pin DHT11 and legacy SHT11 field naming
    dht_temp = serializers.FloatField(required=False)
    dht_humidity = serializers.FloatField(required=False)
    dht_ok = serializers.IntegerField(required=False, default=1)
    
    sht_temp = serializers.FloatField(required=False)
    sht_humidity = serializers.FloatField(required=False)
    sht_ok = serializers.IntegerField(required=False, default=1)
    
    gateway_ts = serializers.IntegerField(required=False)
    rssi = serializers.IntegerField(required=False, default=0)

    def validate(self, attrs):
        # Resolve DHT11 / SHT11 fields gracefully
        if 'dht_temp' in attrs and 'sht_temp' not in attrs:
            attrs['sht_temp'] = attrs['dht_temp']
        if 'dht_humidity' in attrs and 'sht_humidity' not in attrs:
            attrs['sht_humidity'] = attrs['dht_humidity']
        if 'dht_ok' in attrs and 'sht_ok' not in attrs:
            attrs['sht_ok'] = attrs['dht_ok']

        if 'sht_temp' not in attrs:
            raise serializers.ValidationError("Either 'dht_temp' or 'sht_temp' is required.")
        if 'sht_humidity' not in attrs:
            raise serializers.ValidationError("Either 'dht_humidity' or 'sht_humidity' is required.")

        return attrs
