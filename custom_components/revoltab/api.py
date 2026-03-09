import aiohttp

class RevoltabAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://backend.revoltab.com/api/v1"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    async def get_devices(self):
        """Holt alle HIDE Geräte vom Account."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/devices", headers=self.headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                return []

    async def send_command(self, device_id, action):
        """Sende 'open' oder 'close'."""
        data = {"deviceId": device_id, "command": action}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/commands", json=data, headers=self.headers) as resp:
                return resp.status == 200
