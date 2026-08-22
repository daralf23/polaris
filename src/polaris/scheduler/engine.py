from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone
from pathlib import Path
import time

import yaml
from apscheduler.triggers.cron import CronTrigger

from polaris.models.context import PluginContext
from polaris.models.plugin_log import PluginLog
from polaris.services.plugin_manager import PluginManager


def load_discord_config():
    path = Path("config/discord.yaml")

    if not path.exists():
        return None

    with open(path, "r") as f:
        return yaml.safe_load(f)


class SchedulerEngine:
    def __init__(
        self,
        config_loader,
        logger,
        dispatcher,
        state,
    ):
        self.config_loader = config_loader
        self.logger = logger
        self.dispatcher = dispatcher
        self.state = state
        self.plugin_manager = PluginManager()
        self.scheduler = AsyncIOScheduler()

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
                args=[plugin, config, job["name"]],
                **cron,
                id=job["name"],
                name=job["name"],
                replace_existing=True,
            )

        self.scheduler.start()

    async def _run_plugin(
        self,
        plugin,
        config,
        job_name=None,
    ):
        context = PluginContext(
            logger=self.logger,
            config=config,
            http=None,
            dispatcher=self.dispatcher,
            scheduler=self,
            state=self.state,
            job_name=job_name,
        )

        self.logger.info(f"running_plugin:{plugin.name}")

        start = time.time()
        error = None
        events_count = 0

        result = None

        try:
            result = await plugin.run(context, config)

            if result:
                events_count = 1
                await self.dispatcher.send(result)

            status = "success"

        except Exception as e:
            error = str(e)
            status = "error"

        end = time.time()

        log = PluginLog(
            ts=datetime.now(timezone.utc).isoformat(),
            plugin=plugin.name,
            status=status,
            events_emitted=events_count,
            follow_up_seconds=None,
            duration_ms=int((end - start) * 1000),
            error=error,
        )

        self.logger.telemetry(log)

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

    def reschedule_job(
        self,
        plugin_name: str,
        cron: str,
    ):

        job = self.scheduler.get_job(plugin_name)

        if job is None:
            self.logger.warning(
                "job_not_found",
                plugin=plugin_name,
            )
            return

        trigger = CronTrigger.from_crontab(cron)

        job.reschedule(trigger=trigger)

        self.logger.info(
            "job_rescheduled",
            plugin=plugin_name,
            cron=cron,
        )
