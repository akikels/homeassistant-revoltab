from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RevoltabSwitch(data["coordinator"], data["api"])])

class RevoltabSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, api):
        super().__init__(coordinator)
        self._api = api
        device = coordinator.data
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = "Power"
        self._attr_unique_id = f"{self._device_id}_switch"

    @property
    def is_on(self):
        return self.coordinator.data.get("isOn") == 1

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self.coordinator.data.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_turn_on(self, **kwargs):
        if await self._api.send_command("start"):
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        if await self._api.send_command("stop"):
            await self.coordinator.async_request_refresh()
