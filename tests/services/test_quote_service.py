from unittest.mock import AsyncMock

import pytest

from polaris.services.quote_service import QuoteService


QUOTE_URL = "https://example.com/quotes/random"


@pytest.mark.asyncio
async def test_quote_service_returns_quote():

    service = QuoteService()

    service._get_json = AsyncMock(
        return_value=[
            {
                "content": "Testing is good.",
                "author": "Polaris",
            }
        ]
    )

    quote = await service.get_quote(QUOTE_URL)

    service._get_json.assert_awaited_once_with(QUOTE_URL)

    assert quote.content == "Testing is good."
    assert quote.author == "Polaris"


@pytest.mark.asyncio
async def test_quote_service_rejects_empty_response():

    service = QuoteService()

    service._get_json = AsyncMock(return_value=[])

    with pytest.raises(
        ValueError,
        match="no quotes",
    ):
        await service.get_quote(QUOTE_URL)

    service._get_json.assert_awaited_once_with(QUOTE_URL)
