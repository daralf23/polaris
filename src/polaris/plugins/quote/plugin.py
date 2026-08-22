from __future__ import annotations

from polaris.models.event import Event
from polaris.models.quote_config import QuoteConfig
from polaris.plugins.base import BasePlugin
from polaris.services.quote_service import QuoteService


class QuotePlugin(BasePlugin[QuoteConfig]):
    name = "quote"
    config_model = QuoteConfig

    def __init__(self):
        self.quote = QuoteService()

    async def run(
        self,
        context,
        config: QuoteConfig,
    ) -> Event | None:

        try:
            quote = await self.quote.get_quote(config.api_url)

        except Exception as ex:
            context.logger.exception("quote_failed")

            return Event(
                title="Daily Quote Error",
                message=str(ex),
                source=self.name,
            )

        return Event(
            title=config.label,
            message=(f"“{quote.content}”\n— {quote.author}"),
            source=self.name,
        )
