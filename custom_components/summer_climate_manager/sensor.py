from __future__ import annotations
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.util import dt as dt_util
from .entity import SCMEntity
from .const import *
from .logic import fstate, attr_float, summer_active, solar_level, bedroom_decision, open_decision, between_minutes

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        SCMSensor(hass, entry, "strategy", "Strategy"),
        SCMSensor(hass, entry, "solar_level", "Solar Level"),
        SCMSensor(hass, entry, "grid_export", "Grid Export", "W"),
        SCMSensor(hass, entry, "grid_import", "Grid Import", "W"),
        SCMSensor(hass, entry, "ev_power", "EV Charger Power", "W"),
        SCMSensor(hass, entry, "kids_action", "Kids Proposed Action"),
        SCMSensor(hass, entry, "kids_reason", "Kids Reason"),
        SCMSensor(hass, entry, "master_action", "Master Proposed Action"),
        SCMSensor(hass, entry, "master_reason", "Master Reason"),
        SCMSensor(hass, entry, "nursery_action", "Nursery Proposed Action"),
        SCMSensor(hass, entry, "nursery_reason", "Nursery Reason"),
        SCMSensor(hass, entry, "open_action", "Open Plan Proposed Action"),
        SCMSensor(hass, entry, "open_reason", "Open Plan Reason"),
        SCMSensor(hass, entry, "open_eco", "Open Plan Eco Recommendation"),
        SCMSensor(hass, entry, "open_quiet", "Open Plan Quiet Recommendation"),
        SCMFrontendSensor(hass, entry),
    ], True)

class SCMSensor(SCMEntity, SensorEntity):
    def __init__(self, hass, entry, key, name, unit=None):
        super().__init__(hass, entry, key, name)
        if unit:
            self._attr_native_unit_of_measurement = unit
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        d = self.entry.data
        now = dt_util.now()
        export = fstate(self.hass, d.get(CONF_GRID_EXPORT))
        solar = solar_level(export)

        if self.key == "grid_export": return round(export)
        if self.key == "grid_import": return round(fstate(self.hass, d.get(CONF_GRID_IMPORT)))
        if self.key == "ev_power": return round(fstate(self.hass, d.get(CONF_EV_POWER)))
        if self.key == "solar_level": return solar
        if self.key == "strategy":
            if not summer_active(now): return "Out of season"
            return ("High solar pre-cooling" if solar == 3 else
                    "Solar pre-cooling" if solar == 2 else
                    "Light solar pre-cooling" if solar == 1 else "Comfort control")

        if self.key.startswith("kids_"):
            temp = fstate(self.hass, d.get(CONF_KIDS_TEMP))
            dec = bedroom_decision(temp, solar, between_minutes(now, 20*60, 7*60))
            return dec[0] if self.key.endswith("action") else dec[1]

        if self.key.startswith("master_"):
            temp = fstate(self.hass, d.get(CONF_MASTER_TEMP))
            ns = self.hass.states.get("switch.summer_climate_manager_master_night_shift")
            night_shift = bool(ns and ns.state == "on")
            dec = bedroom_decision(temp, solar, between_minutes(now, 22*60+30, 7*60), night_shift)
            return dec[0] if self.key.endswith("action") else dec[1]

        if self.key.startswith("nursery_"):
            temp = fstate(self.hass, d.get(CONF_NURSERY_TEMP))
            sl = self.hass.states.get("switch.summer_climate_manager_nursery_sleep")
            sleep = bool(sl and sl.state == "on")
            dec = bedroom_decision(temp, solar, sleep)
            return dec[0] if self.key.endswith("action") else dec[1]

        if self.key.startswith("open_"):
            temp = fstate(self.hass, d.get(CONF_OPEN_TEMP), None) if d.get(CONF_OPEN_TEMP) else attr_float(self.hass, d.get(CONF_OPEN_CLIMATE), "current_temperature")
            action, reason, eco, quiet = open_decision(temp, solar, 8 <= now.hour < 22)
            if self.key == "open_action": return action
            if self.key == "open_reason": return reason
            if self.key == "open_eco": return "ON" if eco else "OFF"
            if self.key == "open_quiet": return "ON" if quiet else "OFF"
        return "unknown"


class SCMFrontendSensor(SCMEntity, SensorEntity):
    """Expose selected source entities to the companion frontend card."""
    def __init__(self, hass, entry):
        super().__init__(hass, entry, "frontend_config", "Frontend Config")
        self._attr_icon = "mdi:floor-plan"
        self._attr_entity_category = None

    @property
    def native_value(self):
        return "ready"

    @property
    def extra_state_attributes(self):
        d = self.entry.data
        return {
            "card_config": {
                "kids": {"climate": d.get(CONF_KIDS_CLIMATE), "temp": d.get(CONF_KIDS_TEMP), "humidity": d.get(CONF_KIDS_HUMIDITY)},
                "nursery": {"climate": d.get(CONF_NURSERY_CLIMATE), "temp": d.get(CONF_NURSERY_TEMP), "humidity": d.get(CONF_NURSERY_HUMIDITY)},
                "master": {"climate": d.get(CONF_MASTER_CLIMATE), "temp": d.get(CONF_MASTER_TEMP), "humidity": d.get(CONF_MASTER_HUMIDITY)},
                "open": {"climate": d.get(CONF_OPEN_CLIMATE), "temp": d.get(CONF_OPEN_TEMP), "humidity": d.get(CONF_OPEN_HUMIDITY), "eco": d.get(CONF_HISENSE_ECO), "quiet": d.get(CONF_HISENSE_QUIET)},
                "energy": {"grid_import": d.get(CONF_GRID_IMPORT), "grid_export": d.get(CONF_GRID_EXPORT), "ev_charging": d.get(CONF_EV_CHARGING), "ev_power": d.get(CONF_EV_POWER)},
            },
            "floorplan_url": "/summer_climate_manager_static/floorplan.png?v=015",
            "card_version": "0.1.5",
        }
