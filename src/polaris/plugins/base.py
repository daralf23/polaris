from abc import ABC
from abc import abstractmethod

from polaris.models.context import PluginContext
from polaris.models.event import Event


class BasePlugin(ABC):

  name: str

  version: str = "0.1"

  @abstractmethod
  async def run(
      self,
      context: PluginContext,
      **kwargs
  ) -> Event | None:
    """Execute the plugin."""