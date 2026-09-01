import os

import discord
from dotenv import load_dotenv

from polaris.models.bot_config import BotConfig
from polaris.bot.commands import handle_message

load_dotenv()


class PolarisBot(discord.Client):
    def __init__(self, scheduler, logger):
        intents = discord.Intents.default()
        intents.message_content = True
        self.scheduler = scheduler
        self.logger = logger

        self._scheduler_started = False

        self.config = BotConfig(
            token=os.environ["DISCORD_TOKEN"],
            channel_id=int(os.environ["DISCORD_CHANNEL_ID"]),
        )

    async def get_notification_channel(self):
        channel = self.get_channel(self.config.channel_id)

        if channel is None:
            channel = await self.fetch_channel(self.config.channel_id)

        return channel

    async def on_ready(self):
        if not self._scheduler_started:
            self.scheduler.start()
            self._scheduler_started = True
            self.logger.info("scheduler_started")

    async def on_message(self, message: discord.Message):
        await handle_message(message)
