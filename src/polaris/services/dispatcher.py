from abc import ABC, abstractmethod

from polaris.models.event import Event


class BaseDispatcher(ABC):
    @abstractmethod
    async def send(self, event: Event):
        pass


class ConsoleDispatcher(BaseDispatcher):
    async def send(self, event: Event):
        print(f"[{event.level}] {event.title}: {event.message}")


class DiscordDispatcher(BaseDispatcher):
    def __init__(self, client):
        self.client = client

    async def send(self, event: Event):
        channel = await self.client.get_notification_channel()

        if channel is None:
            return

        await channel.send(f"**{event.title}**\n{event.message}")
