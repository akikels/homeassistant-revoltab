from homeassistant.components.switch import SwitchEntity
from .api import RevoltabAPI
from .const import DOMAIN, CONF_API_KEY

async def async_setup_entry(hass, entry, async_add_entities):
    api = RevoltabAPI(entry.data[CONF_API_KEY])
    devices = await api.get_devices()
    async_add_entities([RevoltabSwitch(api, d) for d in devices])

class RevoltabSwitch(SwitchEntity):
    def __init__(self, api, device):
        self._api = api
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = device.get("deviceName", "HIDE Device")
        self._attr_unique_id = f"{self._device_id}_switch"
        self._attr_is_on = device.get("isOn") == 1

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._attr_name,
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_turn_on(self, **kwargs):
        if await self._api.send_command("start"):
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        if await self._api.send_command("stop"):
            self._attr_is_on = False
            self.async_write_ha_state()
