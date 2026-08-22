from polaris.models.event import Event
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
                source=self.name,
            )

        periods = forecast.periods[: config.periods]

        lines = []

        for period in periods:
            lines.append(
                (
                    f"**{period.name}**\n"
                    f"{period.short_forecast}\n"
                    f"{period.temperature}°{period.temperature_unit}\n"
                    f"💨 {period.wind_direction} {period.wind_speed}"
                )
            )

        message = "\n\n".join(lines)

        return Event(
            title=f"{config.label} Forecast",
            message=message,
            source=self.name,
        )
