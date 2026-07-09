from __future__ import annotations

import aiohttp


class WeatherService:
    BASE_URL = "https://api.weather.gov"

    def __init__(self):
        self._headers = {
            # NOAA asks clients to identify themselves.
            # We'll eventually make this configurable.
            "User-Agent": "Polaris Discord Bot (personal use)"
        }

    async def _get_json(self, url: str) -> dict:
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()

                return await response.json()

    async def get_forecast(self, latitude: float, longitude: float) -> dict:
        point = await self._get_json(
            f"{self.BASE_URL}/points/{latitude},{longitude}"
        )

        forecast_url = point["properties"]["forecast"]

        return await self._get_json(forecast_url)
    
    async def get_active_alerts(self, latitude: float, longitude: float) -> dict:
        # NOAA alerts are based on zones, but this keeps it simple for now
        url = f"{self.BASE_URL}/alerts/active?point={latitude},{longitude}"

        return await self._get_json(url)