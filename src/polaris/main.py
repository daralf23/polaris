from polaris.bot.client import PolarisBot
from polaris.bot.dispatcher import DiscordDispatcher
from polaris.scheduler.engine import SchedulerEngine
from polaris.services.config_loader import ConfigLoader
from polaris.services.logger import LoggerService
from polaris.services.state_service import StateService


def main():

    logger = LoggerService()

    config_loader = ConfigLoader("config/jobs.yaml")

    state_service = StateService()

    scheduler = SchedulerEngine(
        config_loader=config_loader,
        logger=logger,
        dispatcher=None,
        state=state_service,
    )

    bot = PolarisBot(scheduler=scheduler, logger=logger)

    dispatcher = DiscordDispatcher(bot)

    scheduler.dispatcher = dispatcher

    bot.run(bot.config.token)


if __name__ == "__main__":
    main()
