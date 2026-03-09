import voluptuous as vol
from homeassistant import config_entries
import aiohttp
from .const import DOMAIN, CONF_API_KEY

class RevoltabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            token = user_input[CONF_API_KEY].strip()
            url = "https://backend.revoltab.com/api/v1/devicestatus"
            headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=10) as resp:
                        if resp.status == 200:
                            return self.async_create_entry(title="Revoltab", data={CONF_API_KEY: token})
                        errors["base"] = "invalid_auth"
                except:
                    errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_API_KEY): str}),
            errors=errors
        )
