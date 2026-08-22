from unittest.mock import AsyncMock, MagicMock

import pytest

from polaris.bot.commands import handle_message


def create_message(
    content: str,
    is_bot: bool = False,
):
    message = MagicMock()

    message.content = content
    message.author.bot = is_bot
    message.channel.send = AsyncMock()

    return message


@pytest.mark.asyncio
async def test_hello_command():
    message = create_message("!hello")

    await handle_message(message)

    message.channel.send.assert_awaited_once_with("👋 Hello! Polaris is alive.")


@pytest.mark.asyncio
async def test_hello_command_is_case_insensitive():
    message = create_message("!HeLLo")

    await handle_message(message)

    message.channel.send.assert_awaited_once_with("👋 Hello! Polaris is alive.")


@pytest.mark.asyncio
async def test_bot_messages_are_ignored():
    message = create_message(
        "!hello",
        is_bot=True,
    )

    await handle_message(message)

    message.channel.send.assert_not_awaited()
