import yaml
from pathlib import Path


class ConfigLoader:
    def __init__(self):
        self.base_path = Path("config")

    def load_jobs(self):
        path = self.base_path / "jobs.yaml"

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        return data.get("jobs", [])