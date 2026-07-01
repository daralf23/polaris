from polaris.models.event import Event
from polaris.models.event import EventLevel
from polaris.models.context import PluginContext

from polaris.plugins.base import BasePlugin


class HelloPlugin(BasePlugin):

  name = "hello"

  async def run(
      self,
      context: PluginContext,
      **kwargs
  ):

    context.logger.info(
        "hello_plugin_running"
    )

    return Event(
        level=EventLevel.INFO,
        title="Hello",
        message="Polaris plugin system is working!"
    )