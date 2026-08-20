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
        # ONLINE / RECOVERY
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
            state["download_history"].append(result.download_mbps)

            state["download_history"] = state["download_history"][
                -config.baseline_runs :
            ]

        # --------------------------------------------------
        # RECORD UPLOAD
        # --------------------------------------------------

        if result.upload_mbps is not None:
            state["upload_history"].append(result.upload_mbps)

            state["upload_history"] = state["upload_history"][-config.baseline_runs :]

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

        performance_state = state["performance_state"]

        # --------------------------------------------------
        # DEGRADED
        # --------------------------------------------------

        if current_speed < minimum_speed:
            state["performance_state"] = "degraded"

            self._save_state(
                context,
                state,
            )

            self._update_schedule(
                context,
                config.degraded_poll,
            )

            if performance_state == "normal":
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

            return None

        # --------------------------------------------------
        # RECOVERED
        # --------------------------------------------------

        state["performance_state"] = "normal"

        self._save_state(
            context,
            state,
        )

        self._update_schedule(
            context,
            config.normal_poll,
        )

        if performance_state == "degraded":
            return Event(
                title="✅ Internet Speed Recovered",
                message=(
                    f"Download speed has recovered "
                    f"to {current_speed:.1f} Mbps. "
                    f"Normal baseline is "
                    f"{baseline:.1f} Mbps."
                ),
                source=self.name,
            )

        return None

    def _load_state(
        self,
        context,
    ) -> dict:

        default_state = {
            "previous_online": None,
            "performance_state": "normal",
            "download_history": [],
            "upload_history": [],
        }

        if context.state is None:
            return default_state

        state = context.state.load(self.STATE_KEY)

        return {
            "previous_online": state.get("previous_online"),
            "performance_state": state.get(
                "performance_state",
                "normal",
            ),
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
