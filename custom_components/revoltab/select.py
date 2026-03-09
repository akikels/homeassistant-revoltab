from __future__ import annotations

import logging
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

INTENSITY_STEPS = {
    "Subtle": 0,
    "Gentle": 25,
    "Moderate": 50,
    "Strong": 75,
    "Intense": 100
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Revoltab select platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    api = data["api"]
    
    async_add_entities([RevoltabIntensitySelect(coordinator, api)])

class RevoltabIntensitySelect(CoordinatorEntity, SelectEntity):
    """Representation of a Revoltab intensity select entity."""

    def __init__(self, coordinator, api) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._api = api
        device = coordinator.data
        
        self._attr_name = "Intensity"
        self._attr_unique_id = f"{device.get('deviceId', 'revoltab_default')}_intensity_select"
        self._attr_options = list(INTENSITY_STEPS.keys())
        self._attr_icon = "mdi:flower-tulip"

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        if not self.coordinator.data:
            return None
            
        val = self.coordinator.data.get("intensity", 0)
        if val >= 100: return "Intense"
        if val >= 75: return "Strong"
        if val >= 50: return "Moderate"
        if val >= 25: return "Gentle"
        return "Subtle"

    @property
    def device_info(self):
        """Return device information about this Revoltab device."""
        device = self.coordinator.data
        return {
            "identifiers": {(DOMAIN, device.get("deviceId", "revoltab_default"))},
            "name": device.get("deviceName", "HIDE"),
            "manufacturer": "Revoltab",
            "model": "HIDE",
        }

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        api_value = INTENSITY_STEPS.get(option, 0)
        if await self._api.set_intensity(api_value):
            await self.coordinator.async_request_refresh()
