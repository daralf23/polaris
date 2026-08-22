from unittest.mock import AsyncMock

import pytest

from polaris.models.context import PluginContext
from polaris.models.weather import WeatherConfig
from polaris.models.weather_forecast import (
    ForecastPeriod,
    WeatherForecast,
)
from polaris.plugins.weather_forecast.plugin import WeatherForecastPlugin
from polaris.services.logger import LoggerService


@pytest.mark.asyncio
async def test_forecast_returns_event():

    plugin = WeatherForecastPlugin()

    plugin.weather.get_forecast = AsyncMock(
        return_value=WeatherForecast(
            periods=[
                ForecastPeriod(
                    name="Today",
                    temperature=80,
                    temperature_unit="F",
                    short_forecast="Sunny",
                    detailed_forecast="Sunny",
                    wind_speed="5 mph",
                    wind_direction="S",
                )
            ]
        )
    )

    context = PluginContext(
        logger=LoggerService(),
        config=None,
        dispatcher=None,
        scheduler=None,
        http=None,
    )

    config = WeatherConfig(
        latitude=35.4,
        longitude=-97.5,
        periods=1,
        label="Home",
    )

    event = await plugin.run(context, config)

    assert event.title == "Home Forecast"
    assert "Today" in event.message
