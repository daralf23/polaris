from unittest.mock import AsyncMock

import pytest

from polaris.models.context import PluginContext
from polaris.models.internet_monitor import InternetMonitorConfig
from polaris.models.speed_test import SpeedTestResult
from polaris.plugins.internet_monitor.plugin import (
    InternetMonitorPlugin,
)
from polaris.services.logger import LoggerService
from polaris.services.state_service import StateService


def create_context(tmp_path):

    return PluginContext(
        logger=LoggerService(),
        config=None,
        dispatcher=None,
        scheduler=None,
        http=None,
        state=StateService(str(tmp_path)),
    )


def create_config():

    return InternetMonitorConfig(
        baseline_runs=10,
        degradation_threshold=0.80,
        normal_poll="*/15 * * * *",
        degraded_poll="*/5 * * * *",
        offline_poll="* * * * *",
    )


def create_online_result(
    download=100.0,
    upload=20.0,
    latency=15.0,
):

    return SpeedTestResult(
        online=True,
        latency_ms=latency,
        download_mbps=download,
        upload_mbps=upload,
    )


def create_offline_result():

    return SpeedTestResult(
        online=False,
    )


@pytest.mark.asyncio
async def test_first_successful_run(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_online_result())

    context = create_context(tmp_path)
    config = create_config()

    event = await plugin.run(
        context,
        config,
    )

    assert event is None

    state = context.state.load("internet_monitor")

    assert state["previous_online"] is True
    assert state["download_history"] == [100.0]
    assert state["upload_history"] == [20.0]


@pytest.mark.asyncio
async def test_baseline_builds_without_alert(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_online_result(download=100.0))

    context = create_context(tmp_path)
    config = create_config()

    for _ in range(9):
        event = await plugin.run(
            context,
            config,
        )

        assert event is None

    state = context.state.load("internet_monitor")

    assert len(state["download_history"]) == 9


@pytest.mark.asyncio
async def test_degraded_speed_generates_event(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock()

    # First nine normal measurements.
    plugin.speed_test.run.side_effect = [
        create_online_result(download=100.0) for _ in range(9)
    ] + [create_online_result(download=70.0)]

    context = create_context(tmp_path)
    config = create_config()

    for _ in range(9):
        event = await plugin.run(
            context,
            config,
        )

        assert event is None

    event = await plugin.run(
        context,
        config,
    )

    assert event is not None
    assert event.title == ("⚠️ Internet Speed Degraded")
    assert "70.0 Mbps" in event.message
    assert "100.0 Mbps" in event.message


@pytest.mark.asyncio
async def test_normal_speed_does_not_generate_event(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock()

    plugin.speed_test.run.side_effect = [
        create_online_result(download=100.0) for _ in range(9)
    ] + [create_online_result(download=90.0)]

    context = create_context(tmp_path)
    config = create_config()

    for _ in range(10):
        event = await plugin.run(
            context,
            config,
        )

    assert event is None


@pytest.mark.asyncio
async def test_first_offline_run_generates_event(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_offline_result())

    context = create_context(tmp_path)
    config = create_config()

    # Establish previous online state.
    context.state.save(
        "internet_monitor",
        {
            "previous_online": True,
            "download_history": [],
            "upload_history": [],
        },
    )

    event = await plugin.run(
        context,
        config,
    )

    assert event is not None
    assert event.title == ("🌐 Internet Offline")


@pytest.mark.asyncio
async def test_continued_offline_returns_none(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_offline_result())

    context = create_context(tmp_path)
    config = create_config()

    context.state.save(
        "internet_monitor",
        {
            "previous_online": False,
            "download_history": [],
            "upload_history": [],
        },
    )

    event = await plugin.run(
        context,
        config,
    )

    assert event is None


@pytest.mark.asyncio
async def test_internet_restored_generates_event(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_online_result())

    context = create_context(tmp_path)
    config = create_config()

    context.state.save(
        "internet_monitor",
        {
            "previous_online": False,
            "download_history": [],
            "upload_history": [],
        },
    )

    event = await plugin.run(
        context,
        config,
    )

    assert event is not None
    assert event.title == ("🌐 Internet Restored")


@pytest.mark.asyncio
async def test_offline_does_not_clear_history(
    tmp_path,
):

    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_offline_result())

    context = create_context(tmp_path)
    config = create_config()

    context.state.save(
        "internet_monitor",
        {
            "previous_online": True,
            "download_history": [
                100.0,
                101.0,
                99.0,
            ],
            "upload_history": [
                20.0,
                21.0,
                19.0,
            ],
        },
    )

    await plugin.run(
        context,
        config,
    )

    state = context.state.load("internet_monitor")

    assert state["previous_online"] is False

    assert state["download_history"] == [
        100.0,
        101.0,
        99.0,
    ]

    assert state["upload_history"] == [
        20.0,
        21.0,
        19.0,
    ]


@pytest.mark.asyncio
async def test_repeated_degradation_returns_none(
    tmp_path,
):
    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_online_result(download=70.0))

    context = create_context(tmp_path)
    config = create_config()

    context.state.save(
        "internet_monitor",
        {
            "previous_online": True,
            "performance_state": "degraded",
            "download_history": [
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
            ],
            "upload_history": [],
        },
    )

    event = await plugin.run(
        context,
        config,
    )

    assert event is None


@pytest.mark.asyncio
async def test_degraded_speed_recovery_generates_event(
    tmp_path,
):
    plugin = InternetMonitorPlugin()

    plugin.speed_test.run = AsyncMock(return_value=create_online_result(download=100.0))

    context = create_context(tmp_path)
    config = create_config()

    context.state.save(
        "internet_monitor",
        {
            "previous_online": True,
            "performance_state": "degraded",
            "download_history": [
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
                100.0,
            ],
            "upload_history": [],
        },
    )

    event = await plugin.run(
        context,
        config,
    )

    assert event is not None
    assert event.title == ("✅ Internet Speed Recovered")
    assert "100.0 Mbps" in event.message
