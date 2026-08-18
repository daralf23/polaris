from __future__ import annotations

from polaris.models.event import Event
from polaris.models.weather import WeatherConfig
from polaris.plugins.base import BasePlugin
from polaris.services.weather_service import WeatherService


class WeatherAlertPlugin(BasePlugin[WeatherConfig]):
    name = "weather_alert"
    config_model = WeatherConfig

    def __init__(self):
        self.weather = WeatherService()
        self.current_schedule = None
        self.known_alert_ids: set[str] = set()
        self._state_initialized = False

    async def run(
        self,
        context,
        config: WeatherConfig,
    ) -> Event | None:

        if not self._state_initialized:
            state = context.state.load(self.name)

            self.known_alert_ids = set(
                state.get(
                    "known_alert_ids",
                    [],
                )
            )

            self._state_initialized = True

        alerts = await self.weather.get_active_alerts(
            config.latitude,
            config.longitude,
        )

        current_ids = set()

        new_alerts = []

        for alert in alerts:
            current_ids.add(alert.id)

            if alert.id not in self.known_alert_ids:
                new_alerts.append(alert)

        cleared_alert_ids = list(self.known_alert_ids - current_ids)

        self.known_alert_ids = current_ids

        context.state.save(
            self.name,
            {"known_alert_ids": list(self.known_alert_ids)},
        )

        desired_schedule = config.alert_poll if current_ids else config.normal_poll

        if context.scheduler and desired_schedule != self.current_schedule:
            context.scheduler.reschedule_job(
                self.name,
                desired_schedule,
            )

            self.current_schedule = desired_schedule

        if not new_alerts and not cleared_alert_ids:
            return None

        lines: list[str] = []

        if new_alerts:
            lines.append("🚨 **New Alerts**")

            for alert in new_alerts:
                lines.append(f"• **{alert.event}**\n  {alert.headline}")

        if cleared_alert_ids:
            if lines:
                lines.append("")

            lines.append("✅ **Cleared Alerts**")

            for alert_id in cleared_alert_ids:
                lines.append(f"• {alert_id}")

        return Event(
            title="Weather Alert Update",
            message="\n".join(lines),
            source=self.name,
        )
