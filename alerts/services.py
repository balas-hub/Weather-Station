import math
from django.utils import timezone
from .models import HistoricalExtremeEvent, HazardAlert
from .dispatcher import dispatch_all_channels

HISTORICAL_CATALOG = [
    {
        "name": "December 2015 Chennai Mega Floods",
        "event_date": "Dec 1 - 4, 2015",
        "category": "Flood",
        "synopsis": "Catastrophic monsoonal depression over Southwest Bay of Bengal stalled off the Tamil Nadu coast, dumping over 494 mm of rain in 24 hours. The Adyar river and Chembarambakkam reservoir overflowed, inundating widespread lowlands across Chennai and Poonamallee.",
        "peak_rainfall_mm": 494.0,
        "barometric_drop_3h": -4.2,
        "peak_humidity_pct": 98.0,
        "peak_heat_index": 33.0,
        "pressure_trend_signature": [-0.5, -1.2, -2.1, -3.4, -4.2, -5.1, -5.8, -6.2],
        "safety_advisory": "Move valuables to higher ground. Disconnect non-critical electrical supplies. Avoid waterlogged transit corridors. Stock potable water and battery backups."
    },
    {
        "name": "2016 Cyclone Vardah (Very Severe Cyclonic Storm)",
        "event_date": "Dec 12, 2016",
        "category": "Cyclone",
        "synopsis": "Made direct landfall just north of Chennai with sustained wind speeds of 130 km/h and gusts over 140 km/h. Characterized by an extraordinary barometric collapse from 1010 hPa down to 975 hPa at the eyewall.",
        "peak_rainfall_mm": 224.0,
        "barometric_drop_3h": -9.8,
        "peak_humidity_pct": 96.0,
        "peak_heat_index": 34.0,
        "pressure_trend_signature": [-1.0, -2.8, -5.2, -8.1, -11.5, -14.2, -18.0, -22.0],
        "safety_advisory": "Take shelter in reinforced structures. Stay away from unfastened glass windows, trees, and transmission towers. Expect power and telecommunication blackouts."
    },
    {
        "name": "2020 Cyclone Nivar",
        "event_date": "Nov 25, 2020",
        "category": "Cyclone",
        "synopsis": "Severe tropical cyclone causing torrential rain bands across coastal Tamil Nadu and extensive water accumulation in urban Chennai.",
        "peak_rainfall_mm": 310.0,
        "barometric_drop_3h": -6.5,
        "peak_humidity_pct": 97.0,
        "peak_heat_index": 32.0,
        "pressure_trend_signature": [-0.8, -1.9, -3.8, -5.5, -7.2, -9.0, -10.5, -11.8],
        "safety_advisory": "Avoid underpasses and low-lying transit routes. Keep portable devices charged and follow IMD regional bulletins."
    },
    {
        "name": "December 2023 Cyclone Michaung Urban Deluge",
        "event_date": "Dec 3 - 5, 2023",
        "category": "Flood",
        "synopsis": "Slow-moving super-dense cloud cluster brought relentless 450 mm rain over 36 hours. Severe urban sheet flooding paralyzed transportation across Chennai, Ambattur, and Poonamallee basin.",
        "peak_rainfall_mm": 450.0,
        "barometric_drop_3h": -5.6,
        "peak_humidity_pct": 99.0,
        "peak_heat_index": 31.0,
        "pressure_trend_signature": [-0.6, -1.8, -3.1, -4.8, -5.6, -6.8, -7.5, -8.0],
        "safety_advisory": "Maintain adequate drinking water and dry rations. Do not wade through moving floodwaters due to open storm drains."
    },
    {
        "name": "May 2024 Extreme Coastal Heatwave & Moisture Shock",
        "event_date": "May 26 - 30, 2024",
        "category": "Heatwave",
        "synopsis": "High surface temperatures (41.5°C) paired with high coastal sea-breeze humidity resulted in lethal Heat Index values exceeding 48°C, posing critical heatstroke risks.",
        "peak_rainfall_mm": 0.0,
        "barometric_drop_3h": 0.2,
        "peak_humidity_pct": 74.0,
        "peak_heat_index": 48.5,
        "pressure_trend_signature": [0.1, 0.0, -0.2, 0.1, 0.2, 0.3, 0.1, 0.0],
        "safety_advisory": "Avoid direct outdoor exertion between 11:00 AM and 3:30 PM. Maintain continuous electrolyte hydration and shelter elderly individuals."
    }
]

def seed_historical_events_if_empty():
    """Populates historical extreme weather baseline events if not already created."""
    if HistoricalExtremeEvent.objects.count() == 0:
        for event in HISTORICAL_CATALOG:
            HistoricalExtremeEvent.objects.create(
                name=event["name"],
                event_date=event["event_date"],
                category=event["category"],
                synopsis=event["synopsis"],
                peak_rainfall_mm=event["peak_rainfall_mm"],
                barometric_drop_3h=event["barometric_drop_3h"],
                peak_humidity_pct=event["peak_humidity_pct"],
                peak_heat_index=event["peak_heat_index"],
                pressure_trend_signature=event["pressure_trend_signature"],
                safety_advisory=event["safety_advisory"]
            )

def find_best_historical_match(pressure_trend_3h: float, humidity: float, heat_index: float, hazard_type: str):
    """
    Computes atmospheric signature similarity using multi-attribute distance metrics
    against known Chennai regional historical disasters.
    """
    seed_historical_events_if_empty()
    events = HistoricalExtremeEvent.objects.all()
    if not events.exists():
        return None, 0.0

    best_event = None
    highest_similarity = 0.0

    for ev in events:
        # Distance calculation
        dp_diff = abs(pressure_trend_3h - ev.barometric_drop_3h)
        hum_diff = abs(humidity - ev.peak_humidity_pct) / 20.0
        hi_diff = abs(heat_index - ev.peak_heat_index) / 15.0

        if 'Heat' in hazard_type or ev.category == 'Heatwave':
            # Weight heat index higher
            composite_dist = (hi_diff * 0.6) + (hum_diff * 0.3) + (dp_diff * 0.1)
        else:
            # Weight pressure drop and humidity highest
            composite_dist = (dp_diff * 0.55) + (hum_diff * 0.35) + (hi_diff * 0.1)

        # Convert distance to percentage similarity [0% to 100%]
        sim = max(0.0, min(99.0, 100.0 * math.exp(-composite_dist / 3.0)))
        
        # Boost if hazard category matches
        if ('Cyclone' in hazard_type and ev.category == 'Cyclone') or \
           ('Flood' in hazard_type and ev.category == 'Flood') or \
           ('Heat' in hazard_type and ev.category == 'Heatwave'):
            sim = min(98.5, sim + 10.0)

        if sim > highest_similarity:
            highest_similarity = sim
            best_event = ev

    return best_event, round(highest_similarity, 1)

def evaluate_telemetry_for_hazards(reading) -> bool:
    """
    Evaluates incoming real-time sensor reading for hazard thresholds.
    Creates and dispatches a HazardAlert if thresholds are exceeded.
    """
    # Prevent alert spam: check if an alert was triggered in the last 45 minutes
    forty_five_mins_ago = timezone.now() - timezone.timedelta(minutes=45)
    recent_active = HazardAlert.objects.filter(created_at__gte=forty_five_mins_ago, is_active=True).first()
    if recent_active:
        return False

    hazard_type = None
    severity = 'MEDIUM'
    title = ""
    description = ""

    # 1. Barometric Pressure Crash (Tropical Storm / Cyclone Warning)
    # Typically > 4.0 hPa drop in 3 hours indicates intense convection or approaching storm
    if reading.pressure_trend_3h <= -6.0 or (reading.bmp_ok and reading.bmp_pressure < 995.0):
        hazard_type = "Severe Storm / Cyclone Approach"
        severity = "CRITICAL"
        title = "Severe Barometric Pressure Drop Detected"
        description = (f"Local barometric pressure has crashed to {reading.bmp_pressure:.1f} hPa "
                       f"with a rapid 3-hour plunge of {reading.pressure_trend_3h:.1f} hPa. "
                       f"Ambient humidity is {reading.sht_humidity:.1f}%. High probability of intense storm or squall.")

    elif reading.pressure_trend_3h <= -3.5:
        hazard_type = "Developing Storm / Monsoonal Squall"
        severity = "HIGH"
        title = "Steep Barometric Fall Observed"
        description = (f"Barometer falling rapidly by {reading.pressure_trend_3h:.1f} hPa over the last 3 hours. "
                       f"Current reading: {reading.bmp_pressure:.1f} hPa.")

    # 2. Extreme Thermal Stress / Heat Index
    elif reading.heat_index >= 45.0:
        hazard_type = "Critical Heatwave & Thermal Stress"
        severity = "CRITICAL"
        title = "Dangerous Heat Index Alert"
        description = (f"The apparent temperature (Heat Index) has soared to {reading.heat_index:.1f}°C "
                       f"(Actual Temp: {reading.fused_temp:.1f}°C, Humidity: {reading.sht_humidity:.1f}%). "
                       f"Heat exhaustion or heatstroke imminent with prolonged physical exposure.")

    elif reading.heat_index >= 41.0:
        hazard_type = "High Heat Index Warning"
        severity = "MEDIUM"
        title = "Elevated Heat Stress Condition"
        description = (f"Heat Index has reached {reading.heat_index:.1f}°C. Practice caution during outdoor activities.")

    # 3. Moisture Saturation & Flood Susceptibility
    elif reading.sht_humidity >= 96.0 and reading.pressure_trend_3h <= -2.0:
        hazard_type = "Heavy Inundation & Rain Squall Risk"
        severity = "HIGH"
        title = "Moisture Saturation with Falling Pressure"
        description = (f"Relative humidity is saturated at {reading.sht_humidity:.1f}% alongside falling pressure "
                       f"({reading.pressure_trend_3h:.1f} hPa). Potential for concentrated downpour and water accumulation.")

    if not hazard_type:
        return False

    # Find historical pattern analog
    best_event, sim_score = find_best_historical_match(
        reading.pressure_trend_3h, reading.sht_humidity, reading.heat_index, hazard_type
    )

    alert = HazardAlert.objects.create(
        hazard_type=hazard_type,
        severity=severity,
        title=title,
        description=description,
        trigger_temp=reading.fused_temp,
        trigger_humidity=reading.sht_humidity,
        trigger_pressure=reading.bmp_pressure,
        trigger_pressure_trend=reading.pressure_trend_3h,
        matched_event_name=best_event.name if best_event else None,
        matched_event_date=best_event.event_date if best_event else None,
        matched_event_impact=best_event.synopsis if best_event else None,
        pattern_similarity_pct=sim_score,
        is_active=True
    )

    # Multi-channel dispatch
    dispatch_all_channels(alert)
    return True
