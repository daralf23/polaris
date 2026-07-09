from pathlib import Path

import yaml


class ConfigLoader:

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

    def load(self) -> dict:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}"
            )

        with open(self.config_path, "r") as file:
            return yaml.safe_load(file) or {}

    def load_jobs(self) -> list:
        config = self.load()

        return config.get("jobs", [])