from __future__ import annotations

from pydantic import BaseModel


class QuoteConfig(BaseModel):
    api_url: str = "https://api.quotable.io/quotes/random"
    label: str = "Daily Quote"
