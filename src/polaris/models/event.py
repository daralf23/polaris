from datetime import UTC, datetime
from pydantic import BaseModel, Field
from enum import Enum


class EventLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Event(BaseModel):
    title: str
    message: str
    level: EventLevel = EventLevel.INFO
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    source: str | None = None
