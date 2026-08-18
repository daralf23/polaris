from __future__ import annotations

import discord


async def handle_message(
    message: discord.Message,
) -> None:
    if message.author.bot:
        return

    command = message.content.strip().casefold()

    if command == "!hello":
        await message.channel.send("👋 Hello! Polaris is alive.")
