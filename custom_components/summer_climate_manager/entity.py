from __future__ import annotations
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class SCMEntity(Entity):
    _attr_has_entity_name = True

    def __init__(self, hass, entry, key, name):
        self.hass = hass
        self.entry = entry
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Summer Climate Manager",
            "manufacturer": "Custom",
            "model": "Summer Climate Manager",
        }

    @property
    def available(self):
        return True
