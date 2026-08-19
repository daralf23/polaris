from unittest.mock import AsyncMock

import pytest

from polaris.models.speed_test import SpeedTestResult
from polaris.models.speed_test_config import SpeedTestConfig
from polaris.services.speed_test_service import SpeedTestService


def test_calculate_mbps():

    result = SpeedTestService._calculate_mbps(
        total_bytes=10_000_000,
        elapsed_seconds=1,
    )

    assert result == 80.0


def test_calculate_mbps_returns_none_for_zero_time():

    result = SpeedTestService._calculate_mbps(
        total_bytes=10_000_000,
        elapsed_seconds=0,
    )

    assert result is None


def test_calculate_mbps_returns_none_for_negative_time():

    result = SpeedTestService._calculate_mbps(
        total_bytes=10_000_000,
        elapsed_seconds=-1,
    )

    assert result is None


@pytest.mark.asyncio
async def test_run_when_offline():

    service = SpeedTestService()
    config = SpeedTestConfig()

    service.check_connectivity = AsyncMock(
        return_value=False,
    )

    result = await service.run(config)

    assert isinstance(result, SpeedTestResult)
    assert result.online is False
    assert result.latency_ms is None
    assert result.download_mbps is None
    assert result.upload_mbps is None

    service.check_connectivity.assert_awaited_once_with(
        config,
    )


@pytest.mark.asyncio
async def test_run_when_online():

    service = SpeedTestService()
    config = SpeedTestConfig()

    service.check_connectivity = AsyncMock(
        return_value=True,
    )

    service.measure_latency = AsyncMock(
        return_value=15.5,
    )

    service.measure_download = AsyncMock(
        return_value=100.0,
    )

    service.measure_upload = AsyncMock(
        return_value=20.0,
    )

    result = await service.run(config)

    assert result.online is True
    assert result.latency_ms == 15.5
    assert result.download_mbps == 100.0
    assert result.upload_mbps == 20.0

    service.check_connectivity.assert_awaited_once_with(
        config,
    )

    service.measure_latency.assert_awaited_once_with(
        config,
    )

    service.measure_download.assert_awaited_once_with(
        config,
    )

    service.measure_upload.assert_awaited_once_with(
        config,
    )


@pytest.mark.asyncio
async def test_run_when_measurements_fail():

    service = SpeedTestService()
    config = SpeedTestConfig()

    service.check_connectivity = AsyncMock(
        return_value=True,
    )

    service.measure_latency = AsyncMock(
        return_value=None,
    )

    service.measure_download = AsyncMock(
        return_value=None,
    )

    service.measure_upload = AsyncMock(
        return_value=None,
    )

    result = await service.run(config)

    assert result.online is True
    assert result.latency_ms is None
    assert result.download_mbps is None
    assert result.upload_mbps is None
