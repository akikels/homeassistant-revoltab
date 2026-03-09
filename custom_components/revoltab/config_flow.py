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
            # 1. API Key säubern (wichtig!)
            api_key = user_input[CONF_API_KEY].replace(" ", "").strip()
            
            # 2. Test-Anfrage an den Revoltab-Server
            # Wir nutzen den Endpunkt, den Jannes im Forum erwähnt hat
            url = "https://backend.revoltab.com/api/v1/devices"
            
            # Wir senden beide gängigen Header-Varianten zur Sicherheit
            headers = {
                "X-API-KEY": api_key,
                "x-api-key": api_key,
                "Accept": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=15) as resp:
                        _LOGGER.debug("Revoltab Test Status: %s", resp.status)
                        
                        if resp.status == 200:
                            # Erfolg! Key speichern
                            return self.async_create_entry(
                                title="Revoltab Cloud", 
                                data={CONF_API_KEY: api_key}
                            )
                        elif resp.status == 401 or resp.status == 403:
                            errors["base"] = "invalid_auth"
                        else:
                            _LOGGER.error("Revoltab API returned status: %s", resp.status)
                            errors["base"] = "cannot_connect"
                except Exception as e:
                    _LOGGER.error("Connection to Revoltab failed: %s", e)
                    errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str
            }),
            errors=errors,
        )
