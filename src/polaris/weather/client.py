import httpx
from .models import BASE_URL, ZoneInfo
from typing import Any, Dict, Optional

class WeatherBug:
    def __init__(self, zone_id: str, zone_type: str = "public"):
        self.zone_type = zone_type
        self.zone_id = zone_id

    # -----------------------------
    # Internal GET helper
    # -----------------------------
    async def _get(self, endpoint: str) -> Dict[str, Any]:
        url = f"{BASE_URL}{endpoint}"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers={"User-Agent": "PolarisBot/1.0"})
            resp.raise_for_status()
            return resp.json()

    async def get_zone_info(self) -> ZoneInfo:
        data = await self._get(f"/zones/{self.zone_type}/{self.zone_id}")

        return ZoneInfo(
            id=data["id"],
            name=data["properties"]["name"],
            type=data["properties"]["type"],
            state=data["properties"]["state"],
        )

    async def get_forecast(self) -> Dict[str, Any]:
        return await self._get(
            f"/zones/{self.zone_type}/{self.zone_id}/forecast"
        )

    async def get_hourly_forecast(self) -> Dict[str, Any]:
        return await self._get(
            f"/zones/{self.zone_type}/{self.zone_id}/forecast/hourly"
        )

    async def get_alerts(self) -> Dict[str, Any]:
        return await self._get(
            f"/alerts/active/zone/{self.zone_id}"
        )

    async def get_daily_summary(self) -> str:
        forecast = await self.get_forecast()
        periods = forecast["properties"]["periods"]

        summary = []
        for p in periods[:3]:  # Next 3 periods
            summary.append(f"**{p['name']}**: {p['detailedForecast']}")

        return "\n\n".join(summary)