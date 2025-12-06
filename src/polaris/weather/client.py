import requests
from .models import ForecastPeriod, ThreeDayForecast

class ForecastClient:
    BASE_URL = "https://api.weather.gov"

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def _get_forecast_url(self) -> str:
        """Retrieve the forecast URL for this point."""
        url = f"{self.BASE_URL}/points/{self.lat},{self.lon}"
        resp = requests.get(url, headers={"User-Agent": "PolarisBot/1.0"})
        resp.raise_for_status()

        data = resp.json()
        return data["properties"]["forecast"]

    def get_three_day_forecast(self) -> ThreeDayForecast:
        """Fetch 3 days (6 periods) of forecasts."""
        forecast_url = self._get_forecast_url()

        resp = requests.get(forecast_url, headers={"User-Agent": "PolarisBot/1.0"})
        resp.raise_for_status()

        data = resp.json()
        periods = data["properties"]["periods"]

        # Only use the first 6 periods → approx. 3 days
        selected = periods[:6]

        result = [
            ForecastPeriod(
                name=p["name"],
                temperature=p["temperature"],
                temperature_unit=p["temperatureUnit"],
                short_forecast=p["shortForecast"],
            )
            for p in selected
        ]

        return ThreeDayForecast(periods=result)