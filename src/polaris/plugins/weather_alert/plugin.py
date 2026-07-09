import aiohttp

from polaris.models.event import Event
from polaris.models.plugin_result import PluginResult
from polaris.models.weather import WeatherConfig
from polaris.plugins.base import BasePlugin
from polaris.services.weather_service import WeatherService

import json
from pathlib import Path

class WeatherAlertPlugin(BasePlugin[WeatherConfig]):
    name = "weather_alert"
    config_model = WeatherConfig
    STATE_FILE = Path("data/weather_alert_state.json")

    def __init__(self):
        self.weather = WeatherService()
        self._state_loaded = False
        self.known_alert_ids = set()
        # in-memory state (we'll persist later)
        self.known_alert_ids: set[str] = set()

    def load_state(self):
        if not self.STATE_FILE.exists():
            self.known_alert_ids = set()
            return

        try:
            with open(self.STATE_FILE, "r") as f:
                data = json.load(f)

            self.known_alert_ids = set(data.get("known_alert_ids", []))

        except Exception:
            # fail safe: don't break plugin if file is corrupt
            self.known_alert_ids = set()

    def save_state(self):
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "known_alert_ids": list(self.known_alert_ids)
        }

        with open(self.STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    async def run(self, context, config: WeatherConfig):

        if not self._state_loaded:
            self.load_state()
            self._state_loaded = True

        data = await self.weather.get_active_alerts(
            config.latitude,
            config.longitude,
        )

        features = data.get("features", [])

        current_ids = set()
        events = []

        # ---------------------------
        # 1. Parse current alerts
        # ---------------------------
        for alert in features:
            alert_id = alert["id"]
            current_ids.add(alert_id)

            if alert_id not in self.known_alert_ids:
                props = alert["properties"]

                events.append(
                    Event(
                        title=f"🚨 {props.get('event', 'Weather Alert')}",
                        message=props.get("headline", "New weather alert"),
                    )
                )

        # ---------------------------
        # 2. Detect expired alerts
        # ---------------------------
        expired = self.known_alert_ids - current_ids

        for alert_id in expired:
            events.append(
                Event(
                    title="Weather Alert Cleared",
                    message=f"Alert ended: {alert_id}",
                )
            )

        # ---------------------------
        # 3. Update state
        # ---------------------------
        self.known_alert_ids = current_ids

        # ---------------------------
        # 4. Decide polling frequency
        # ---------------------------
        if current_ids:
            follow_up = 60      # active weather → check often
        else:
            follow_up = 900     # calm weather → slow polling

        # ---------------------------
        # 5. Return result
        # ---------------------------
        self.save_state()
        return PluginResult(
            events=events,
            follow_up_seconds=follow_up,
        )