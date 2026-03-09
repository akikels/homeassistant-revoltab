from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RevoltabIntensity(data["coordinator"], data["api"])])

class RevoltabIntensity(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, api):
        super().__init__(coordinator)
        self._api = api
        device = coordinator.data
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = "Intensity"
        self._attr_unique_id = f"{self._device_id}_intensity"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1

    @property
    def native_value(self):
        data = self.coordinator.data
        val = data.get("intensity") if data.get("intensity") is not None else data.get("Intensity")
        return float(val) if val is not None else 0.0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self.coordinator.data.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_set_native_value(self, value: float) -> None:
        if await self._api.set_intensity(int(value)):
            await self.coordinator.async_request_refresh()
