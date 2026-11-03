from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import HazardAlert, HistoricalExtremeEvent
from .services import seed_historical_events_if_empty, find_best_historical_match
from .dispatcher import (
    dispatch_all_channels, 
    send_telegram_alert, 
    get_telegram_config, 
    save_telegram_config
)

class ActiveAlertsAPIView(APIView):
    """
    Returns active hazard alerts.
    Endpoint: GET /api/alerts/active/
    """
    def get(self, request):
        seed_historical_events_if_empty()
        alerts = HazardAlert.objects.filter(is_active=True).order_by('-created_at')[:5]
        data = []
        for a in alerts:
            data.append({
                "id": a.id,
                "created_at": a.created_at.isoformat(),
                "hazard_type": a.hazard_type,
                "severity": a.severity,
                "title": a.title,
                "description": a.description,
                "trigger_metrics": {
                    "temp": a.trigger_temp,
                    "humidity": a.trigger_humidity,
                    "pressure": a.trigger_pressure,
                    "trend_3h": a.trigger_pressure_trend
                },
                "matched_historical_event": {
                    "name": a.matched_event_name,
                    "date": a.matched_event_date,
                    "impact": a.matched_event_impact,
                    "similarity_pct": a.pattern_similarity_pct
                } if a.matched_event_name else None,
                "channels": a.channels_dispatched
            })
        return Response({"active_alerts": data, "count": len(data)})

class AcknowledgeAlertAPIView(APIView):
    """
    Dismisses/acknowledges an active alert.
    Endpoint: POST /api/alerts/<id>/dismiss/
    """
    def post(self, request, alert_id):
        try:
            alert = HazardAlert.objects.get(id=alert_id)
            alert.is_active = False
            alert.acknowledged_at = timezone.now()
            alert.save(update_fields=['is_active', 'acknowledged_at'])
            return Response({"status": "acknowledged"})
        except HazardAlert.DoesNotExist:
            return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)

class ClearAllAlertsAPIView(APIView):
    """
    Dismisses all active alerts back to normal status.
    Endpoint: POST /api/alerts/clear/
    """
    def post(self, request):
        now = timezone.now()
        count = HazardAlert.objects.filter(is_active=True).update(is_active=False, acknowledged_at=now)
        return Response({"status": "cleared", "count": count})

class HistoricalEventsCatalogAPIView(APIView):
    """
    Returns the catalog of Chennai historical disaster events and their atmospheric signatures.
    Endpoint: GET /api/alerts/historical-catalog/
    """
    def get(self, request):
        seed_historical_events_if_empty()
        events = HistoricalExtremeEvent.objects.all().order_by('-id')
        data = []
        for ev in events:
            data.append({
                "id": ev.id,
                "name": ev.name,
                "date": ev.event_date,
                "category": ev.category,
                "synopsis": ev.synopsis,
                "peak_rainfall_mm": ev.peak_rainfall_mm,
                "barometric_drop_3h": ev.barometric_drop_3h,
                "peak_humidity_pct": ev.peak_humidity_pct,
                "peak_heat_index": ev.peak_heat_index,
                "signature": ev.pressure_trend_signature,
                "safety_advisory": ev.safety_advisory
            })
        return Response({"events": data})

class SimulateAlertAPIView(APIView):
    """
    Endpoint to simulate real atmospheric hazard conditions (Storm, Heatwave, Flood)
    for verifying mobile push, sounds, vibration, and Telegram alert delivery.
    Endpoint: POST /api/alerts/simulate/
    """
    def post(self, request):
        scenario = request.data.get('scenario', 'storm').lower()
        seed_historical_events_if_empty()

        # Clear older alerts to focus on the newly simulated hazard
        HazardAlert.objects.filter(is_active=True).update(is_active=False)

        if scenario in ['heat', 'heatwave']:
            hz_type = "Dangerous Coastal Heatwave Alert"
            sev = "CRITICAL"
            title = "Extreme Heat Stress & Thermal Emergency"
            desc = "Ambient temperature reached 42.8°C with 74% humidity. Heat Index exceeded 48.5°C danger threshold."
            dp = 0.2
            hum = 74.0
            temp = 42.8
            pres = 1008.2
            hi = 48.5
        elif scenario in ['flood', 'rain', 'deluge']:
            hz_type = "Severe Urban Flood & Inundation Warning"
            sev = "HIGH"
            title = "Moisture Saturation with Rapid Pressure Plunge"
            desc = "Relative humidity saturated at 98.5% with falling barometric pressure (-4.6 hPa in 3h). Torrential monsoonal downpour likely."
            dp = -4.6
            hum = 98.5
            temp = 29.2
            pres = 1002.4
            hi = 34.0
        else: # storm / cyclone
            hz_type = "Severe Cyclonic Storm & Squall Warning"
            sev = "CRITICAL"
            title = "Catastrophic Barometric Drop Detected"
            desc = "Local barometer dropped rapidly to 992.5 hPa with a 3-hour plunge of -8.4 hPa. Squalls and damaging gusts expected."
            dp = -8.4
            hum = 96.0
            temp = 30.5
            pres = 992.5
            hi = 35.0

        best_event, sim = find_best_historical_match(dp, hum, hi, hz_type)

        alert = HazardAlert.objects.create(
            hazard_type=hz_type,
            severity=sev,
            title=title,
            description=desc,
            trigger_temp=temp,
            trigger_humidity=hum,
            trigger_pressure=pres,
            trigger_pressure_trend=dp,
            matched_event_name=best_event.name if best_event else None,
            matched_event_date=best_event.event_date if best_event else None,
            matched_event_impact=best_event.synopsis if best_event else None,
            pattern_similarity_pct=sim,
            is_active=True
        )

        channels = dispatch_all_channels(alert)
        return Response({
            "status": "alert_created",
            "alert_id": alert.id,
            "scenario": scenario,
            "title": alert.title,
            "severity": alert.severity,
            "description": alert.description,
            "trigger_metrics": {
                "temperature": temp,
                "humidity": hum,
                "pressure": pres,
                "pressure_trend_3h": dp
            },
            "matched_event": alert.matched_event_name,
            "similarity_pct": alert.pattern_similarity_pct,
            "dispatched_channels": channels
        }, status=status.HTTP_201_CREATED)

class TelegramConfigAPIView(APIView):
    """
    Gets or updates the Telegram Bot notification configuration.
    Endpoint: GET, POST /api/alerts/telegram/
    """
    def get(self, request):
        cfg = get_telegram_config()
        token = cfg.get("bot_token", "")
        # Mask token for security
        masked_token = f"{token[:6]}...{token[-4:]}" if len(token) > 12 else token
        return Response({
            "configured": bool(cfg.get("bot_token") and cfg.get("chat_id")),
            "enabled": cfg.get("enabled", False),
            "chat_id": cfg.get("chat_id", ""),
            "masked_token": masked_token
        })

    def post(self, request):
        bot_token = request.data.get("bot_token", "").strip()
        chat_id = request.data.get("chat_id", "").strip()
        enabled = request.data.get("enabled", True)

        if not bot_token or not chat_id:
            return Response({
                "error": "Both bot_token and chat_id are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        save_telegram_config(bot_token, chat_id, enabled)
        return Response({
            "status": "success",
            "message": "Telegram alert settings saved successfully!",
            "chat_id": chat_id,
            "enabled": enabled
        })

class TelegramTestAlertAPIView(APIView):
    """
    Sends an immediate test notification to verify Telegram setup.
    Endpoint: POST /api/alerts/telegram/test/
    """
    def post(self, request):
        custom_token = request.data.get("bot_token")
        custom_chat_id = request.data.get("chat_id")

        success, msg = send_telegram_alert(
            title="Weather Station Test Notification",
            message="✅ Your Telegram alert setup is working perfectly! You will receive emergency alerts here when hazards are detected.",
            historical_note="Poonamallee Weather Observatory AI Monitoring Station",
            custom_token=custom_token,
            custom_chat_id=custom_chat_id
        )

        if success:
            return Response({"status": "success", "message": msg})
        else:
            return Response({"status": "failed", "message": msg}, status=status.HTTP_400_BAD_REQUEST)
