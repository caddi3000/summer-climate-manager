from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt as dt_util
from .entity import SCMEntity
from .const import *
from .logic import summer_active

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        SCMBinary(hass, entry, "summer_season", "Summer Season"),
        SCMBinary(hass, entry, "ev_charging", "EV Charging"),
    ], True)

class SCMBinary(SCMEntity, BinarySensorEntity):
    @property
    def is_on(self):
        if self.key == "summer_season":
            return summer_active(dt_util.now())
        ent = self.entry.data.get(CONF_EV_CHARGING)
        st = self.hass.states.get(ent) if ent else None
        return bool(st and st.state == "on")
