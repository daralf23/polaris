from pydantic import BaseModel

from polaris.models.event import Event
from polaris.models.context import PluginContext
from polaris.plugins.base import BasePlugin


class HelloConfig(BaseModel):
    message: str = "Polaris is working!"


class HelloPlugin(BasePlugin[HelloConfig]):
    name = "hello"
    version = "0.1"

    config_model = HelloConfig

    async def run(self, context: PluginContext, config: HelloConfig):

        context.logger.info("hello_plugin_running")

        return Event(
            title="Hello World",
            message="Test Hello World",
        )
