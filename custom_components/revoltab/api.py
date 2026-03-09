import aiohttp

class RevoltabAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://backend.revoltab.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json"
        }

    async def get_device_status(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/devicestatus", headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                return None

    async def send_command(self, action):
        endpoint = "startdevice" if action == "start" else "stopdevice"
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/{endpoint}", headers=self.headers) as resp:
                return resp.status == 200

    async def set_intensity(self, value):
        data = {"value": str(value)}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/setintensity", 
                headers=self.headers, 
                data=data
            ) as resp:
                return resp.status == 200
