from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from polaris.models.event import Event


@dataclass
class PluginResult:
    events: list[Event] = field(default_factory=list)

    # Optional one-time follow-up run
    follow_up: timedelta | None = None