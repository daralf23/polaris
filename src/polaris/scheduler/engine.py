import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from polaris.services.plugin_manager import PluginManager
from polaris.models.context import PluginContext

from polaris.services.dispatcher import ConsoleDispatcher

class SchedulerEngine:
    def __init__(self, config_loader, logger):
        self.config_loader = config_loader
        self.logger = logger

        self.dispatcher = ConsoleDispatcher()

        self.scheduler = AsyncIOScheduler()
        self.plugin_manager = PluginManager()

    def start(self):
        self.logger.info("scheduler_starting")

        plugins = self.plugin_manager.discover()
        jobs = self.config_loader.load_jobs()

        for job in jobs:
            if not job.get("enabled", True):
                continue

            plugin = plugins.get(job["plugin"])
            if not plugin:
                self.logger.warning(f"plugin_not_found:{job['plugin']}")
                continue

            config_model = plugin.config_model
            config = config_model.model_validate(job.get("config", {}))
            cron = self._parse_cron(job["schedule"])

            self.scheduler.add_job(
                self._run_plugin,
                trigger="cron",
                args=[plugin, config],
                **cron,
                id=job["name"],
                replace_existing=True,
            )

        self.scheduler.start()

    async def _run_plugin(self, plugin, config):
        context = PluginContext(
            logger=self.logger,
            config=config,
            http=None,
            dispatcher=None,
        )

        self.logger.info(f"running_plugin:{plugin.name}")

        event = await plugin.run(context, config)

        if event:
            event.source = plugin.name
            await self.dispatcher.send(event)

    def _parse_cron(self, cron_expr: str):
        # "0 7 * * *"
        minute, hour, day, month, dow = cron_expr.split()

        return {
            "minute": minute,
            "hour": hour,
            "day": day,
            "month": month,
            "day_of_week": dow,
        }