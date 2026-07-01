from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EventLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Event(BaseModel):
    title: str
    message: str
    level: EventLevel = EventLevel.INFO
    timestamp: datetime = datetime.utcnow()

    source: str | None = None  # plugin name