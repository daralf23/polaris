from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from polaris.bot.commands import handle_message


def create_message(
    content: str,
    is_bot: bool = False,
):
    message = MagicMock(spec=discord.Message)

    message.author = MagicMock()
    message.author.bot = is_bot
    message.content = content

    message.channel = MagicMock()
    message.channel.send = AsyncMock()

    return message


@pytest.mark.asyncio
async def test_hello_command():

    message = create_message("!Hello")

    await handle_message(message)

    message.channel.send.assert_awaited_once_with("👋 Hello! Polaris is alive.")


@pytest.mark.asyncio
async def test_hello_command_is_case_insensitive():

    message = create_message("!HELLO")

    await handle_message(message)

    message.channel.send.assert_awaited_once_with("👋 Hello! Polaris is alive.")


@pytest.mark.asyncio
async def test_bot_messages_are_ignored():

    message = create_message(
        "!Hello",
        is_bot=True,
    )

    await handle_message(message)

    message.channel.send.assert_not_awaited()
