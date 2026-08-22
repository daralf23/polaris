from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WeatherAlert:
    id: str
    headline: str
    event: str
    severity: str
    urgency: str
    certainty: str
    description: str
    instruction: str | None
    sent: datetime
    expires: datetime
