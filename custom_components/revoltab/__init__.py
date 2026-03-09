from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .api import RevoltabAPI
from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    api = RevoltabAPI(entry.data[CONF_API_KEY])

    async def async_update_data():
        """Zentrale Datenabfrage."""
        return await api.get_device_status()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="revoltab_device",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    # Hier wurde "sensor" hinzugefügt
    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "number", "sensor"])
    return True

async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, ["switch", "number", "sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
