import pytest

from polaris.plugins.hello.plugin import HelloPlugin


@pytest.mark.asyncio
async def test_hello_plugin_returns_event(plugin_context):

    plugin = HelloPlugin()

    event = await plugin.run(
        plugin_context,
        {"message": "Test Hello World"},
    )

    assert event is not None
    assert event.message == "Test Hello World"
