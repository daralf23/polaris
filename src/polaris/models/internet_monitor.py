from pydantic import BaseModel, Field

from polaris.models.speed_test_config import SpeedTestConfig


class InternetMonitorConfig(BaseModel):
    normal_poll: str = "*/15 * * * *"
    degraded_poll: str = "*/5 * * * *"
    offline_poll: str = "* * * * *"

    baseline_runs: int = 10
    degradation_threshold: float = 0.20

    speed_test: SpeedTestConfig = Field(
        default_factory=SpeedTestConfig,
    )