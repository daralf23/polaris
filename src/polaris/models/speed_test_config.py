from __future__ import annotations

from pydantic import BaseModel


class SpeedTestConfig(BaseModel):
    connectivity_url: str = "https://www.google.com/generate_204"

    download_url: str = "https://speed.cloudflare.com/__down?bytes=10000000"

    upload_url: str = "https://speed.cloudflare.com/__up"

    download_bytes: int = 10_000_000

    upload_bytes: int = 2_000_000
