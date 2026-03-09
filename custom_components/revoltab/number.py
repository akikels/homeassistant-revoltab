from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

STEP_TO_API = {1: 0, 2: 25, 3: 50, 4: 75, 5: 100}

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RevoltabIntensityNumber(data["coordinator"], data["api"])])

class RevoltabIntensityNumber(CoordinatorEntity, NumberEntity):
    _attr_has_entity_name = True
    _attr_name = "Intensity Level"

    def __init__(self, coordinator, api):
        super().__init__(coordinator)
        self._api = api
        device = coordinator.data
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_unique_id = f"{self._device_id}_intensity_number_steps"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 5
        self._attr_native_step = 1
        self._attr_icon = "mdi:gauge"

    @property
    def native_value(self):
        val = self.coordinator.data.get("intensity", 0)
        if val >= 100: return 5
        if val >= 75: return 4
        if val >= 50: return 3
        if val >= 25: return 2
        return 1

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self.coordinator.data.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_set_native_value(self, value: float) -> None:
        api_value = STEP_TO_API.get(int(value), 0)
        if await self._api.set_intensity(api_value):
            await self.coordinator.async_request_refresh()