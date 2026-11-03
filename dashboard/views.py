import socket
from django.shortcuts import render
from django.conf import settings

def get_local_ip():
    """Detects local LAN IP of the host machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip

def index_view(request):
    """Renders the real-time Hardware Observatory Dashboard."""
    local_ip = get_local_ip()
    context = {
        "station_name": getattr(settings, 'STATION_NAME', 'Poonamallee Weather Observatory, Chennai'),
        "latitude": getattr(settings, 'STATION_LATITUDE', 13.089017),
        "longitude": getattr(settings, 'STATION_LONGITUDE', 80.102193),
        "elevation_m": 22.0,
        "local_ip": local_ip,
        "ingest_url": f"http://{local_ip}:8000/api/sensors/readings/",
        "station_secret": getattr(settings, 'STATION_API_SECRET', 'weather-station-secret-key-2026')
    }
    return render(request, 'dashboard/index.html', context)
