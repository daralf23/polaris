from polaris.models.event import Event
from polaris.models.plugin_result import PluginResult
from polaris.models.weather import WeatherConfig
from polaris.plugins.base import BasePlugin
from polaris.services.weather_service import WeatherService


class WeatherForecastPlugin(BasePlugin[WeatherConfig]):
    name = "weather_forecast"
    config_model = WeatherConfig

    def __init__(self):
        self.weather = WeatherService()

    async def run(self, context, config: WeatherConfig):
        try:
            forecast = await self.weather.get_forecast(
                config.latitude,
                config.longitude,
            )

        except Exception as ex:
            context.logger.exception("weather_forecast_failed")

            return Event(
                title="Weather Error",
                message=str(ex),
            )

        periods = forecast["properties"]["periods"][:config.periods]

        lines = []

        for period in periods:
            lines.append(
                f"{period['name']}: "
                f"{period['shortForecast']} "
                f"{period['temperature']}°{period['temperatureUnit']}"
            )

        return PluginResult(
            events=[
                Event(
                    title="Forecast",
                    message=message,
                )
            ]
        )