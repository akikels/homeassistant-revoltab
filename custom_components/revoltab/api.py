import aiohttp

class RevoltabAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://backend.revoltab.com/api/v1"
        self.headers = {
            "X-API-KEY": self.api_key.strip(),
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    async def get_devices(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/devices", headers=self.headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                return []

    async def send_command(self, device_id, action):
        # Swagger nutzt oft 'open' oder 'close' für HIDE Produkte
        data = {"deviceId": device_id, "command": action}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/commands", json=data, headers=self.headers) as resp:
                return resp.status == 200 or resp.status == 201
