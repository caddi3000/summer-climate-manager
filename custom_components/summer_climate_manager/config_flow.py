from __future__ import annotations
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import *

ENTITY = selector.EntitySelector

class SummerClimateManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="Summer Climate Manager", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_GRID_IMPORT): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Required(CONF_GRID_EXPORT): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_EV_CHARGING): ENTITY(selector.EntitySelectorConfig(domain="binary_sensor")),
            vol.Optional(CONF_EV_POWER): ENTITY(selector.EntitySelectorConfig(domain="sensor")),

            vol.Required(CONF_KIDS_CLIMATE): ENTITY(selector.EntitySelectorConfig(domain="climate")),
            vol.Required(CONF_KIDS_TEMP): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_KIDS_HUMIDITY): ENTITY(selector.EntitySelectorConfig(domain="sensor")),

            vol.Required(CONF_NURSERY_CLIMATE): ENTITY(selector.EntitySelectorConfig(domain="climate")),
            vol.Required(CONF_NURSERY_TEMP): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_NURSERY_HUMIDITY): ENTITY(selector.EntitySelectorConfig(domain="sensor")),

            vol.Required(CONF_MASTER_CLIMATE): ENTITY(selector.EntitySelectorConfig(domain="climate")),
            vol.Required(CONF_MASTER_TEMP): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_MASTER_HUMIDITY): ENTITY(selector.EntitySelectorConfig(domain="sensor")),

            vol.Required(CONF_OPEN_CLIMATE): ENTITY(selector.EntitySelectorConfig(domain="climate")),
            vol.Optional(CONF_OPEN_TEMP): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_OPEN_HUMIDITY): ENTITY(selector.EntitySelectorConfig(domain="sensor")),
            vol.Optional(CONF_HISENSE_ECO): ENTITY(selector.EntitySelectorConfig(domain="switch")),
            vol.Optional(CONF_HISENSE_QUIET): ENTITY(selector.EntitySelectorConfig(domain="switch")),
        })
        return self.async_show_form(step_id="user", data_schema=schema)
