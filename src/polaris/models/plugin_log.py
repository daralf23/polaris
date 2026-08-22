from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PluginLog:
    ts: str
    plugin: str
    status: str
    events_emitted: int = 0
    follow_up_seconds: Optional[int] = None
    duration_ms: int = 0
    error: Optional[str] = None

    def to_json(self) -> dict:
        return asdict(self)
