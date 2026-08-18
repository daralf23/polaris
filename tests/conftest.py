from unittest.mock import AsyncMock, Mock

import pytest

from polaris.models.context import PluginContext
from polaris.models.weather import WeatherConfig
from polaris.services.logger import LoggerService
from polaris.services.state_service import StateService
from polaris.services.config_loader import ConfigLoader


@pytest.fixture
def logger():
    return LoggerService()


@pytest.fixture
def state(tmp_path):
    return StateService(base_path=str(tmp_path))


@pytest.fixture
def weather_config():
    return WeatherConfig(
        latitude=35.0,
        longitude=-97.0,
        label="Home",
    )


@pytest.fixture
def mock_scheduler():
    return Mock()


@pytest.fixture
def plugin_context(
    logger,
    state,
    mock_scheduler,
):
    return PluginContext(
        logger=logger,
        config=None,
        dispatcher=None,
        scheduler=mock_scheduler,
        http=None,
        state=state,
    )


@pytest.fixture
def dispatcher():
    return AsyncMock()


@pytest.fixture
def config_loader(tmp_path):
    config_file = tmp_path / "jobs.yaml"
    config_file.write_text("jobs: []\n")

    return ConfigLoader(str(config_file))
