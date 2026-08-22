from __future__ import annotations

import aiohttp

from polaris.models.quote import Quote


class QuoteService:
    async def _get_json(self, url: str) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                return await response.json()

    async def get_quote(
        self,
        api_url: str,
    ) -> Quote:

        data = await self._get_json(api_url)

        if not data:
            raise ValueError("Quote API returned no quotes")

        quote = data[0]

        return Quote(
            content=quote["content"],
            author=quote["author"],
        )
