from unittest.mock import AsyncMock

import pytest

from polaris.models.context import PluginContext
from polaris.models.weather import WeatherConfig
from polaris.models.weather_alert import WeatherAlert
from polaris.plugins.weather_alert.plugin import WeatherAlertPlugin
from polaris.services.logger import LoggerService
from polaris.services.state_service import StateService


@pytest.fixture
def weather_config():
    return WeatherConfig(
        latitude=35,
        longitude=-97,
        label="Home",
    )


@pytest.fixture
def plugin_context(tmp_path):
    return PluginContext(
        logger=LoggerService(),
        config=None,
        dispatcher=None,
        scheduler=None,
        http=None,
        state=StateService(base_path=str(tmp_path)),
    )


@pytest.mark.asyncio
async def test_new_alert_generates_event(
    plugin_context,
    weather_config,
):

    plugin = WeatherAlertPlugin()

    plugin.weather.get_active_alerts = AsyncMock(
        return_value=[
            WeatherAlert(
                id="abc",
                headline="Tornado Warning",
                event="Tornado Warning",
                severity="Extreme",
                urgency="Immediate",
                certainty="Observed",
                description="...",
                instruction="...",
                sent=None,
                expires=None,
            )
        ]
    )

    event = await plugin.run(
        plugin_context,
        weather_config,
    )

    assert event is not None
    assert "Tornado" in event.message


@pytest.mark.asyncio
async def test_duplicate_alert_returns_none(
    plugin_context,
    weather_config,
):

    plugin = WeatherAlertPlugin()

    plugin_context.state.save(
        plugin.name,
        {
            "known_alert_ids": ["abc"],
        },
    )

    plugin.weather.get_active_alerts = AsyncMock(
        return_value=[
            WeatherAlert(
                id="abc",
                headline="Tornado Warning",
                event="Tornado Warning",
                severity="Extreme",
                urgency="Immediate",
                certainty="Observed",
                description="...",
                instruction="...",
                sent=None,
                expires=None,
            )
        ]
    )

    event = await plugin.run(
        plugin_context,
        weather_config,
    )

    assert event is None


@pytest.mark.asyncio
async def test_cleared_alert_generates_event(
    plugin_context,
    weather_config,
):

    plugin = WeatherAlertPlugin()

    plugin_context.state.save(
        plugin.name,
        {
            "known_alert_ids": ["abc"],
        },
    )

    plugin.weather.get_active_alerts = AsyncMock(return_value=[])

    event = await plugin.run(
        plugin_context,
        weather_config,
    )

    assert event is not None
    assert event.title == "Weather Alert Update"
    assert "Cleared" in event.message
    assert "abc" in event.message


@pytest.mark.asyncio
async def test_alert_state_persists_between_runs(
    plugin_context,
    weather_config,
):

    first_plugin = WeatherAlertPlugin()

    first_plugin.weather.get_active_alerts = AsyncMock(
        return_value=[
            WeatherAlert(
                id="abc",
                headline="Tornado Warning",
                event="Tornado Warning",
                severity="Extreme",
                urgency="Immediate",
                certainty="Observed",
                description="...",
                instruction="...",
                sent=None,
                expires=None,
            )
        ]
    )

    first_event = await first_plugin.run(
        plugin_context,
        weather_config,
    )

    assert first_event is not None

    second_plugin = WeatherAlertPlugin()

    second_plugin.weather.get_active_alerts = AsyncMock(
        return_value=[
            WeatherAlert(
                id="abc",
                headline="Tornado Warning",
                event="Tornado Warning",
                severity="Extreme",
                urgency="Immediate",
                certainty="Observed",
                description="...",
                instruction="...",
                sent=None,
                expires=None,
            )
        ]
    )

    second_event = await second_plugin.run(
        plugin_context,
        weather_config,
    )

    assert second_event is None
