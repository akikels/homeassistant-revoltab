import voluptuous as vol
from homeassistant import config_entries
import aiohttp
import logging
from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

class RevoltabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api_key = user_input[CONF_API_KEY].strip() # Leerzeichen entfernen
            
            # Teste die Verbindung
            url = "https://backend.revoltab.com/api/v1/devices"
            headers = {
                "X-API-KEY": api_key,
                "accept": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=10) as resp:
                        if resp.status == 200:
                            return self.async_create_entry(title="Revoltab", data={CONF_API_KEY: api_key})
                        else:
                            _LOGGER.error("Revoltab API Fehler: Status %s", resp.status)
                            errors["base"] = "invalid_auth"
                except Exception as e:
                    _LOGGER.error("Revoltab Verbindung fehlgeschlagen: %s", e)
                    errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str
            }),
            errors=errors,
        )
