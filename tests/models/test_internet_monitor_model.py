from polaris.models.internet_monitor import InternetMonitorConfig
from polaris.models.speed_test_config import SpeedTestConfig


def test_internet_monitor_has_default_speed_test_config():

    config = InternetMonitorConfig()

    assert isinstance(config.speed_test, SpeedTestConfig)

    assert (
        config.speed_test.connectivity_url
        == "https://www.google.com/generate_204"
    )

    assert (
        config.speed_test.download_url
        == "https://speed.cloudflare.com/__down?bytes=10000000"
    )

    assert (
        config.speed_test.upload_url
        == "https://speed.cloudflare.com/__up"
    )

    assert config.speed_test.download_bytes == 10_000_000
    assert config.speed_test.upload_bytes == 2_000_000