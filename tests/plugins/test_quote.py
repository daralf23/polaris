from unittest.mock import AsyncMock

import pytest

from polaris.models.quote import Quote
from polaris.models.quote_config import QuoteConfig
from polaris.plugins.quote.plugin import QuotePlugin


@pytest.mark.asyncio
async def test_quote_plugin_generates_event(
    plugin_context,
):

    plugin = QuotePlugin()

    plugin.quote_service.get_quote = AsyncMock(
        return_value=Quote(
            content="Testing is good.",
            author="Polaris",
        )
    )

    config = QuoteConfig()

    event = await plugin.run(
        plugin_context,
        config,
    )

    assert event is not None
    assert event.title == "💡 Daily Quote"
    assert "Testing is good." in event.message
    assert "Polaris" in event.message
    assert event.source == "quote"


@pytest.mark.asyncio
async def test_quote_plugin_handles_api_failure(
    plugin_context,
):

    plugin = QuotePlugin()

    plugin.quote_service.get_quote = AsyncMock(
        side_effect=RuntimeError("API unavailable")
    )

    config = QuoteConfig()

    event = await plugin.run(
        plugin_context,
        config,
    )

    assert event is not None
    assert event.title == "💡 Daily Quote"
    assert "couldn't retrieve" in event.message
