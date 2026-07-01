from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PluginContext:
  logger: Any
  config: Any
  http: Any
  dispatcher: Any