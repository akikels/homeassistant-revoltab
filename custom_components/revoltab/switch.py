from homeassistant.components.switch import SwitchEntity
from .api import RevoltabAPI
from .const import DOMAIN, CONF_API_KEY

async def async_setup_entry(hass, entry, async_add_entities):
    # Hier wird der Key aus der Konfiguration geholt, den du im Fenster eingegeben hast
    api_key = entry.data[CONF_API_KEY]
    api = RevoltabAPI(api_key)
    
    devices = await api.get_devices()
    entities = [RevoltabDevice(api, d) for d in devices]
    async_add_entities(entities)

class RevoltabDevice(SwitchEntity):
    def __init__(self, api, device):
        self._api = api
        self._device = device
        self._attr_name = device.get("name", f"HIDE {device['id']}")
        self._attr_unique_id = f"revoltab_{device['id']}"
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        if await self._api.send_command(self._device["id"], "open"):
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        if await self._api.send_command(self._device["id"], "close"):
            self._is_on = False
            self.async_write_ha_state()
