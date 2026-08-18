from __future__ import annotations

from polaris.models.event import Event
from polaris.models.quote_config import QuoteConfig
from polaris.plugins.base import BasePlugin
from polaris.services.quote_service import QuoteService


class QuotePlugin(BasePlugin[QuoteConfig]):
    name = "quote"
    config_model = QuoteConfig

    def __init__(self):
        self.quote_service = QuoteService()

    async def run(
        self,
        context,
        config: QuoteConfig,
    ) -> Event:

        try:
            quote = await self.quote_service.get_quote(
                config.api_url,
            )

        except Exception:
            context.logger.exception(
                "quote_failed",
            )

            return Event(
                title="💡 Daily Quote",
                message=("I couldn't retrieve today's quote."),
                source=self.name,
            )

        return Event(
            title="💡 Daily Quote",
            message=(f'"{quote.content}"\n— {quote.author}'),
            source=self.name,
        )
