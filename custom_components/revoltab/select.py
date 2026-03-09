from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

INTENSITY_STEPS = {
    "Subtle": 0,
    "Gentle": 25,
    "Moderate": 50,
    "Strong": 75,
    "Intense": 100
}

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RevoltabIntensitySelect(data["coordinator"], data["api"])])

class RevoltabIntensitySelect(CoordinatorEntity, SelectEntity):
    def __init__(self, coordinator, api):
        super().__init__(coordinator)
        self._api = api
        device = coordinator.data
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = "Intensity"
        self._attr_unique_id = f"{self._device_id}_intensity_select"
        self._attr_options = list(INTENSITY_STEPS.keys())
        self._attr_icon = "mdi:flower-tulip"

    @property
    def current_option(self):
        val = self.coordinator.data.get("intensity", 0)
        if val >= 100: return "Intense"
        if val >= 75: return "Strong"
        if val >= 50: return "Moderate"
        if val >= 25: return "Gentle"
        return "Subtle"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self.coordinator.data.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_select_option(self, option: str) -> None:
        api_value = INTENSITY_STEPS.get(option, 0)
        if await self._api.set_intensity(api_value):
            await self.coordinator.async_request_refresh()
