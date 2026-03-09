from homeassistant.components.number import NumberEntity
from .const import DOMAIN, CONF_API_KEY

async def async_setup_entry(hass, entry, async_add_entities):
    from .api import RevoltabAPI
    api = RevoltabAPI(entry.data[CONF_API_KEY])
    devices = await api.get_devices()
    async_add_entities([RevoltabIntensity(api, d) for d in devices])

class RevoltabIntensity(NumberEntity):
    def __init__(self, api, device):
        self._api = api
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = "Intensity" # Name innerhalb des Geräts
        self._attr_unique_id = f"{self._device_id}_intensity"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_native_value = device.get("intensity", 50)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._api_device_name, # Nutzt den Namen des Geräts
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_set_native_value(self, value: float) -> None:
        if await self._api.set_intensity(int(value)):
            self._attr_native_value = value
            self.async_write_ha_state()
