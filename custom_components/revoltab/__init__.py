from .const import DOMAIN

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "number"])
    return True

async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_forward_entry_unload(entry, ["switch", "number"])
