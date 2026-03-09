import voluptuous as vol
from homeassistant import config_entries
import aiohttp
from .const import DOMAIN, CONF_API_KEY

class RevoltabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Behandelt die Einrichtung über die Benutzeroberfläche."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Hier prüfen wir kurz, ob der Key gültig ist
            api_key = user_input[CONF_API_KEY]
            is_valid = await self._test_api_key(api_key)
            
            if is_valid:
                return self.async_create_entry(title="Revoltab Cloud", data=user_input)
            else:
                errors["base"] = "invalid_auth"

        # Das ist das Formular, das in HA erscheint
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str
            }),
            errors=errors,
        )

    async def _test_api_key(self, api_key):
        """Testet den Key gegen die Revoltab API."""
        url = "https://backend.revoltab.com/api/v1/devices"
        headers = {"X-API-KEY": api_key}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as resp:
                    return resp.status == 200
            except:
                return False
