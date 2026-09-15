from __future__ import annotations
from pathlib import Path

from homeassistant.components.http import StaticPathConfig

from .const import DOMAIN, PLATFORMS

FRONTEND_URL = f"/{DOMAIN}"

async def async_setup_entry(hass, entry):
    frontend_dir = Path(__file__).parent / "frontend"
    await hass.http.async_register_static_paths([
        StaticPathConfig(FRONTEND_URL, str(frontend_dir), False)
    ])

    # Load the companion Lovelace card automatically. This avoids requiring
    # a separate HACS frontend repository/resource entry.
    hass.data.setdefault("frontend_extra_module_url", set()).add(
        f"{FRONTEND_URL}/summer-climate-floorplan.js?v=0.1.3"
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
