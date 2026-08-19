from __future__ import annotations

from statistics import mean

from polaris.models.event import Event
from polaris.models.internet_monitor import InternetMonitorConfig
from polaris.plugins.base import BasePlugin
from polaris.services.speed_test_service import SpeedTestService


class InternetMonitorPlugin(BasePlugin[InternetMonitorConfig]):
    name = "internet_monitor"
    config_model = InternetMonitorConfig

    STATE_KEY = "internet_monitor"

    def __init__(self):
        self.speed_test = SpeedTestService()
        self.current_schedule: str | None = None

    async def run(
        self,
        context,
        config: InternetMonitorConfig,
    ) -> Event | None:

        state = self._load_state(context)

        result = await self.speed_test.run(config.speed_test)

        previous_online = state["previous_online"]
        download_history = state["download_history"]
        upload_history = state["upload_history"]

        # --------------------------------------------------
        # OFFLINE
        # --------------------------------------------------

        if not result.online:
            state["previous_online"] = False

            self._save_state(
                context,
                state,
            )

            self._update_schedule(
                context,
                config.offline_poll,
            )

            if previous_online is True:
                return Event(
                    title="🌐 Internet Offline",
                    message=(
                        "Polaris detected that the Internet connection is offline."
                    ),
                    source=self.name,
                )

            return None

        # --------------------------------------------------
        # RECOVERY
        # --------------------------------------------------

        state["previous_online"] = True

        if previous_online is False:
            self._save_state(
                context,
                state,
            )

            self._update_schedule(
                context,
                config.normal_poll,
            )

            return Event(
                title="🌐 Internet Restored",
                message=("Internet connectivity has been restored."),
                source=self.name,
            )

        # --------------------------------------------------
        # RECORD DOWNLOAD
        # --------------------------------------------------

        if result.download_mbps is not None:
            download_history.append(result.download_mbps)

            state["download_history"] = download_history[-config.baseline_runs :]

        # --------------------------------------------------
        # RECORD UPLOAD
        # --------------------------------------------------

        if result.upload_mbps is not None:
            upload_history.append(result.upload_mbps)

            state["upload_history"] = upload_history[-config.baseline_runs :]

        # --------------------------------------------------
        # NOT ENOUGH DATA FOR BASELINE
        # --------------------------------------------------

        if len(state["download_history"]) < config.baseline_runs:
            self._save_state(
                context,
                state,
            )

            self._update_schedule(
                context,
                config.normal_poll,
            )

            return None

        # --------------------------------------------------
        # CALCULATE BASELINE
        # --------------------------------------------------

        history = state["download_history"]

        current_speed = history[-1]

        baseline = mean(history[:-1])

        minimum_speed = baseline * config.degradation_threshold

        # --------------------------------------------------
        # DEGRADED
        # --------------------------------------------------

        if current_speed < minimum_speed:
            self._save_state(
                context,
                state,
            )

            self._update_schedule(
                context,
                config.degraded_poll,
            )

            return Event(
                title="⚠️ Internet Speed Degraded",
                message=(
                    f"Download speed is "
                    f"{current_speed:.1f} Mbps. "
                    f"Normal baseline is "
                    f"{baseline:.1f} Mbps."
                ),
                source=self.name,
            )

        # --------------------------------------------------
        # NORMAL
        # --------------------------------------------------

        self._save_state(
            context,
            state,
        )

        self._update_schedule(
            context,
            config.normal_poll,
        )

        return None

    def _load_state(
        self,
        context,
    ) -> dict:

        if context.state is None:
            return {
                "previous_online": None,
                "download_history": [],
                "upload_history": [],
            }

        state = context.state.load(self.STATE_KEY)

        return {
            "previous_online": state.get("previous_online"),
            "download_history": state.get(
                "download_history",
                [],
            ),
            "upload_history": state.get(
                "upload_history",
                [],
            ),
        }

    def _save_state(
        self,
        context,
        state: dict,
    ) -> None:

        if context.state is None:
            return

        context.state.save(
            self.STATE_KEY,
            state,
        )

    def _update_schedule(
        self,
        context,
        schedule: str,
    ) -> None:

        if schedule == self.current_schedule:
            return

        if context.scheduler and context.job_name:
            context.scheduler.reschedule_job(
                context.job_name,
                schedule,
            )

        self.current_schedule = schedule
