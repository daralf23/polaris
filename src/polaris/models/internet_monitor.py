from __future__ import annotations

from pydantic import BaseModel


class InternetMonitorConfig(BaseModel):
    normal_poll: str = "*/15 * * * *"
    degraded_poll: str = "*/5 * * * *"
    offline_poll: str = "* * * * *"

    baseline_runs: int = 10
    degradation_threshold: float = 0.20

    speed_test: object | None = None
