from unittest.mock import AsyncMock

import pytest

from polaris.models.context import PluginContext
from polaris.models.quote_config import QuoteConfig
from polaris.models.quote import Quote
from polaris.plugins.quote.plugin import QuotePlugin
from polaris.services.logger import LoggerService


@pytest.fixture
def quote_context():
    return PluginContext(
        logger=LoggerService(),
        config=None,
        dispatcher=None,
        scheduler=None,
        state=None,
        http=None,
    )


@pytest.fixture
def quote_config():
    return QuoteConfig(
        url="https://example.com/quote",
        label="Daily Quote",
    )


@pytest.mark.asyncio
async def test_quote_plugin_returns_event(
    quote_context,
    quote_config,
):
    plugin = QuotePlugin()

    plugin.quote.get_quote = AsyncMock(
        return_value=Quote(
            content="Testing is good.",
            author="Polaris",
        )
    )

    event = await plugin.run(
        quote_context,
        quote_config,
    )

    assert event is not None
    assert event.title == "Daily Quote"
    assert "Testing is good." in event.message
    assert "Polaris" in event.message
    assert event.source == "quote"


@pytest.mark.asyncio
async def test_quote_plugin_handles_service_error(
    quote_context,
    quote_config,
):
    plugin = QuotePlugin()

    plugin.quote.get_quote = AsyncMock(side_effect=Exception("API unavailable"))

    event = await plugin.run(
        quote_context,
        quote_config,
    )

    assert event is not None
    assert event.title == "Daily Quote Error"
    assert "API unavailable" in event.message
    assert event.source == "quote"
