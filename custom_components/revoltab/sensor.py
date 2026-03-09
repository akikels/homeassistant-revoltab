from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        RevoltabFillLevel(data["coordinator"]),
        RevoltabOnlineStatus(data["coordinator"])
    ])

class RevoltabFillLevel(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        device = coordinator.data
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = "Fill Level"
        self._attr_unique_id = f"{self._device_id}_filllevel"
        self._attr_native_unit_of_measurement = "%"
        self._attr_icon = "mdi:water-percent"

    @property
    def native_value(self):
        return self.coordinator.data.get("fillLevel")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self.coordinator.data.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

class RevoltabOnlineStatus(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        device = coordinator.data
        self._device_id = device.get("deviceId", "revoltab_default")
        self._attr_name = "Connectivity"
        self._attr_unique_id = f"{self._device_id}_online"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Gibt True zurück, wenn isOnline im JSON eine 1 ist."""
        return self.coordinator.data.get("isOnline") == 1

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self.coordinator.data.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }
