import discord

from polaris.models.event import Event


class DiscordDispatcher:
    def __init__(self, bot):
        self.bot = bot

    async def send(self, event: Event):

        channel = await self.bot.get_notification_channel()

        embed = discord.Embed(
            title=event.title,
            description=event.message,
        )

        await channel.send(embed=embed)
