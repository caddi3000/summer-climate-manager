from datetime import time
from .const import DEFAULTS

def fstate(hass, entity_id, default=0.0):
    if not entity_id:
        return default
    try:
        return float(hass.states.get(entity_id).state)
    except (AttributeError, TypeError, ValueError):
        return default

def attr_float(hass, entity_id, attr, default=0.0):
    st = hass.states.get(entity_id) if entity_id else None
    try:
        return float(st.attributes.get(attr, default))
    except (AttributeError, TypeError, ValueError):
        return default

def summer_active(now):
    return now.month in (10,11,12,1,2,3,4)

def between_minutes(now, start_min, end_min):
    cur = now.hour * 60 + now.minute
    return (start_min <= cur < end_min) if start_min < end_min else (cur >= start_min or cur < end_min)

def solar_level(export_w):
    if export_w >= DEFAULTS["solar_high_w"]: return 3
    if export_w >= DEFAULTS["solar_medium_w"]: return 2
    if export_w >= DEFAULTS["solar_light_w"]: return 1
    return 0

def bedroom_decision(temp, solar, sleep=False, night_shift=False):
    if night_shift:
        return ("COOL 16°C", "Night-shift day sleep override")
    ceiling = DEFAULTS["bedroom_ceiling"]
    if sleep:
        if temp >= ceiling:
            return ("COOL 24°C", "Sleep comfort ceiling reached")
        if temp >= 24.5:
            return ("COOL 24°C", "Sleep temperature rising")
        return ("OFF", "Sleep - comfortable")
    if temp >= ceiling:
        return ("COOL 24°C", "Bedroom comfort ceiling reached")
    if solar >= 2 and temp >= 23:
        return ("COOL 22°C", "Solar pre-cooling available")
    if solar >= 1 and temp >= 24:
        return ("COOL 23°C", "Light solar pre-cooling")
    return ("OFF", "Within comfort range")

def open_decision(temp, solar, active):
    if not active:
        return ("OFF", "Outside open-plan operating hours", False, False)
    if temp >= 27:
        return ("COOL 24°C", "Open-plan comfort ceiling", False, False)
    if solar >= 2 and temp >= 23.5:
        return ("COOL 22°C", "Solar pre-cooling", False, False)
    if solar >= 1 and temp >= 24.5:
        return ("COOL 23°C", "Light solar pre-cooling", True, False)
    if temp >= 25.5:
        return ("COOL 24°C", "Normal comfort cooling", True, False)
    return ("OFF", "Within comfort range", False, False)
