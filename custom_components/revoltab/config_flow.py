import voluptuous as vol
from homeassistant import config_entries
import aiohttp
import logging
import async_timeout
from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

class RevoltabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api_key = user_input[CONF_API_KEY].replace(" ", "").strip()
            
            # Wir testen die Verbindung
            url = "https://backend.revoltab.com/api/v1/devices"
            headers = {
                "X-API-KEY": api_key,
                "Accept": "application/json",
                "User-Agent": "HomeAssistant-Integration"
            }
            
            async with aiohttp.ClientSession() as session:
                try:
                    # Timeout auf 20 Sekunden erhöhen
                    async with async_timeout.timeout(20):
                        async with session.get(url, headers=headers) as resp:
                            _LOGGER.info("Revoltab API Response: %s", resp.status)
                            
                            if resp.status == 200:
                                return self.async_create_entry(
                                    title="Revoltab Cloud", 
                                    data={CONF_API_KEY: api_key}
                                )
                            elif resp.status in [401, 403]:
                                errors["base"] = "invalid_auth"
                            else:
                                _LOGGER.error("Revoltab API Error %s", resp.status)
                                errors["base"] = "cannot_connect"
                except Exception as e:
                    _LOGGER.error("Revoltab Connection Exception: %s", str(e))
                    errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str
            }),
            errors=errors,
        )
