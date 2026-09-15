from homeassistant.components.select import SelectEntity
from homeassistant.helpers.restore_state import RestoreEntity
from .entity import SCMEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ModeSelect(hass, entry)])

class ModeSelect(SCMEntity, SelectEntity, RestoreEntity):
    _attr_options = ["Off", "Monitor"]
    def __init__(self, hass, entry):
        super().__init__(hass, entry, "mode", "Mode")
        self._attr_current_option = "Monitor"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        old = await self.async_get_last_state()
        if old and old.state in self.options:
            self._attr_current_option = old.state

    async def async_select_option(self, option: str):
        self._attr_current_option = option
        self.async_write_ha_state()
