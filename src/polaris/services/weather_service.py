from __future__ import annotations

import aiohttp
from datetime import datetime

from polaris.models.weather_alert import WeatherAlert


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
        point = await self._get_json(f"{self.BASE_URL}/points/{latitude},{longitude}")

        forecast_url = point["properties"]["forecast"]

        return await self._get_json(forecast_url)

    async def get_active_alerts(
        self,
        latitude: float,
        longitude: float,
    ) -> list[WeatherAlert]:

        url = f"{self.BASE_URL}/alerts/active?point={latitude},{longitude}"

        response = await self._get_json(url)

        alerts = []

        for feature in response.get("features", []):
            props = feature["properties"]

            alerts.append(
                WeatherAlert(
                    id=feature["id"],
                    headline=props["headline"],
                    event=props["event"],
                    severity=props["severity"],
                    urgency=props["urgency"],
                    certainty=props["certainty"],
                    description=props["description"],
                    instruction=props.get("instruction"),
                    sent=datetime.fromisoformat(props["sent"].replace("Z", "+00:00")),
                    expires=datetime.fromisoformat(
                        props["expires"].replace("Z", "+00:00")
                    ),
                )
            )

        return alerts
