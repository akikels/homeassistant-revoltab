import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
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
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return RevoltabOptionsFlowHandler(config_entry)

class RevoltabOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get("scan_interval", 5),
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600)),
            }),
        )