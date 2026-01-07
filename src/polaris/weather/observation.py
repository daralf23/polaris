import httpx
from .models import BASE_URL

class ObservationClient:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    async def _get(self, url: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers={"User-Agent": "Polaris/1.0"})
            r.raise_for_status()
            return r.json()

    async def get_nearest_station(self) -> str:
        data = await self._get(f"{BASE_URL}/points/{self.lat},{self.lon}")
        stations_url = data["properties"]["observationStations"]
        stations = await self._get(stations_url)
        return stations["observationStations"][0].split("/")[-1]

    async def get_latest_observation(self):
        station = await self.get_nearest_station()
        return await self._get(f"{BASE_URL}/stations/{station}/observations/latest")

    async def get_barometric_pressure(self) -> float:
        obs = await self.get_latest_observation()
        pa = obs["properties"]["barometricPressure"]["value"]
        if pa is None:
            return None
        return pa / 100  # hPa