from dataclasses import dataclass
from typing import Any


@dataclass
class PluginContext:
    logger: Any
    config: Any
    http: Any = None
    dispatcher: Any = None
    scheduler: Any = None
    state: Any = None
    job_name: str | None = None
