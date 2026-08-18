from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

from polaris.models.context import PluginContext
from polaris.models.event import Event

ConfigT = TypeVar("ConfigT", bound=BaseModel)


class BasePlugin(Generic[ConfigT], ABC):
    name: str
    version: str = "0.1"

    config_model: type[ConfigT] | None = None

    @abstractmethod
    async def run(
        self,
        context: PluginContext,
        config: ConfigT,
    ) -> Event | None:
        pass
