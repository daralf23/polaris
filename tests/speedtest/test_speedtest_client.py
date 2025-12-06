from unittest.mock import patch, MagicMock
from polaris.speedtest.client import SpeedTestClient
from polaris.speedtest.models import SpeedTestResult

@patch("polaris.speedtest.client.speedtest.Speedtest")
def test_speedtest_client(mock_speedtest):
    # Mock instance returned by Speedtest()
    mock_instance = MagicMock()
    mock_instance.download.return_value = 100_000_000  # 100 Mbps
    mock_instance.upload.return_value = 10_000_000     # 10 Mbps
    mock_instance.results.ping = 25.5

    mock_speedtest.return_value = mock_instance

    client = SpeedTestClient()
    result = client.run_test()

    assert isinstance(result, SpeedTestResult)
    assert result.download_mbps == 100.0
    assert result.upload_mbps == 10.0
    assert result.ping_ms == 25.5