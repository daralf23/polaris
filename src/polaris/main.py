import asyncio
import structlog

from polaris.scheduler.engine import SchedulerEngine
from polaris.config.loader import ConfigLoader


async def main():
    logger = structlog.get_logger()

    config_loader = ConfigLoader()

    engine = SchedulerEngine(config_loader, logger)

    engine.start()

    logger.info("polaris_started")

    while True:
        await asyncio.sleep(3600)  # keep event loop alive


if __name__ == "__main__":
    asyncio.run(main())