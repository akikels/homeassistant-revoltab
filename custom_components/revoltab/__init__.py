from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .api import RevoltabAPI
from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = 10 

async def async_setup_entry(hass: HomeAssistant, entry):
    api = RevoltabAPI(entry.data[CONF_API_KEY])

    async def async_update_data():
        return await api.get_device_status()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="revoltab_device",
        update_method=async_update_data,
        update_interval=timedelta(seconds=SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "select", "number""sensor", "binary_sensor"])
    return True

async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, ["switch", "select", "number", "sensor", "binary_sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
