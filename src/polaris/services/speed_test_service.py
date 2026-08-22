from __future__ import annotations

import time

import aiohttp

from polaris.models.speed_test import SpeedTestResult
from polaris.models.speed_test_config import SpeedTestConfig


class SpeedTestService:
    async def check_connectivity(
        self,
        config: SpeedTestConfig,
    ) -> bool:

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    config.connectivity_url,
                    timeout=aiohttp.ClientTimeout(
                        total=10,
                    ),
                ) as response:
                    return response.status < 500

        except aiohttp.ClientError:
            return False

        except TimeoutError:
            return False

    async def measure_latency(
        self,
        config: SpeedTestConfig,
    ) -> float | None:

        try:
            start = time.perf_counter()

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    config.connectivity_url,
                    timeout=aiohttp.ClientTimeout(
                        total=10,
                    ),
                ) as response:
                    await response.read()

            elapsed = time.perf_counter() - start

            return elapsed * 1000

        except (
            aiohttp.ClientError,
            TimeoutError,
        ):
            return None

    async def measure_download(
        self,
        config: SpeedTestConfig,
    ) -> float | None:

        try:
            start = time.perf_counter()
            total_bytes = 0

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    config.download_url,
                    timeout=aiohttp.ClientTimeout(
                        total=60,
                    ),
                ) as response:
                    async for chunk in response.content.iter_chunked(64 * 1024):
                        total_bytes += len(chunk)

            elapsed = time.perf_counter() - start

            return self._calculate_mbps(
                total_bytes,
                elapsed,
            )

        except (
            aiohttp.ClientError,
            TimeoutError,
        ):
            return None

    async def measure_upload(
        self,
        config: SpeedTestConfig,
    ) -> float | None:

        payload = b"0" * config.upload_bytes

        try:
            start = time.perf_counter()

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config.upload_url,
                    data=payload,
                    timeout=aiohttp.ClientTimeout(
                        total=60,
                    ),
                ) as response:
                    await response.read()

            elapsed = time.perf_counter() - start

            return self._calculate_mbps(
                len(payload),
                elapsed,
            )

        except (
            aiohttp.ClientError,
            TimeoutError,
        ):
            return None

    async def run(
        self,
        config: SpeedTestConfig,
    ) -> SpeedTestResult:

        online = await self.check_connectivity(config)

        if not online:
            return SpeedTestResult(
                online=False,
            )

        latency = await self.measure_latency(config)
        download = await self.measure_download(config)
        upload = await self.measure_upload(config)

        return SpeedTestResult(
            online=True,
            latency_ms=latency,
            download_mbps=download,
            upload_mbps=upload,
        )

    @staticmethod
    def _calculate_mbps(
        total_bytes: int,
        elapsed_seconds: float,
    ) -> float | None:
        if elapsed_seconds <= 0:
            return None

        megabits = total_bytes * 8 / 1_000_000

        return megabits / elapsed_seconds
