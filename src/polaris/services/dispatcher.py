from abc import ABC, abstractmethod
from polaris.models.event import Event
import discord


class BaseDispatcher(ABC):
    @abstractmethod
    async def send(self, event: Event):
        pass

class ConsoleDispatcher(BaseDispatcher):
    async def send(self, event: Event):
        print(f"[{event.level}] {event.title}: {event.message}")



class DiscordDispatcher(BaseDispatcher):
    def __init__(self, token: str, channel_id: int):
        self.token = token
        self.channel_id = channel_id

        self.client = discord.Client(intents=discord.Intents.default())
        self.channel = None

        @self.client.event
        async def on_ready():
            self.channel = self.client.get_channel(channel_id)
            print("Discord connected")

    async def send(self, event: Event):
        if not self.channel:
            return

        await self.channel.send(f"**{event.title}**\n{event.message}")

    def run(self):
        self.client.run(self.token)