from __future__ import annotations

from pydantic import BaseModel


class SpeedTestResult(BaseModel):
    online: bool
    latency_ms: float | None = None
    download_mbps: float | None = None
    upload_mbps: float | None = None
