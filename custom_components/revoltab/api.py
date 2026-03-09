import aiohttp

class RevoltabAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://backend.revoltab.com/api/v1"
        self.headers = {"Authorization": f"Bearer {self.token}", "accept": "application/json"}

    async def get_devices(self):
        """Holt Status (liefert laut Screenshot ein einzelnes Objekt oder Liste)."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/devicestatus", headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Falls es nur ein Gerät ist, packen wir es in eine Liste
                    return [data] if isinstance(data, dict) else data
                return []

    async def send_command(self, action):
        """Action ist 'start' oder 'stop'."""
        endpoint = "startdevice" if action == "start" else "stopdevice"
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/{endpoint}", headers=self.headers) as resp:
                return resp.status == 200

    async def set_intensity(self, value):
        """Setzt die Intensität (0-100) laut Screenshot."""
        # Laut Swagger Bild wird x-www-form-urlencoded mit 'value=X' erwartet
        data = {"value": str(value)}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/setintensity", 
                headers=self.headers, 
                data=data
            ) as resp:
                return resp.status == 200
