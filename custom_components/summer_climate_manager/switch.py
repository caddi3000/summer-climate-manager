from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util import dt as dt_util
from datetime import timedelta
from .entity import SCMEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        LocalSwitch(hass, entry, "master_night_shift", "Master Night Shift", auto_off_at_15=True),
        LocalSwitch(hass, entry, "nursery_sleep", "Nursery Sleep"),
    ])

class LocalSwitch(SCMEntity, SwitchEntity, RestoreEntity):
    def __init__(self, hass, entry, key, name, auto_off_at_15=False):
        super().__init__(hass, entry, key, name)
        self._is_on = False
        self.auto_off_at_15 = auto_off_at_15
        self._cancel = None

    @property
    def is_on(self): return self._is_on

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        old = await self.async_get_last_state()
        self._is_on = bool(old and old.state == "on")
        if self._is_on and self.auto_off_at_15:
            self._schedule_off()

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()
        if self.auto_off_at_15: self._schedule_off()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        if self._cancel:
            self._cancel(); self._cancel = None
        self.async_write_ha_state()

    def _schedule_off(self):
        if self._cancel: self._cancel()
        now = dt_util.now()
        target = now.replace(hour=15, minute=0, second=0, microsecond=0)
        if target <= now: target += timedelta(days=1)
        async def cb(_now):
            self._is_on = False
            self._cancel = None
            self.async_write_ha_state()
        self._cancel = async_track_point_in_time(self.hass, cb, target)
