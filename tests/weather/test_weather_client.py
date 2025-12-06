import json
from unittest.mock import patch
from polaris.weather.client import ForecastClient
from polaris.weather.models import ThreeDayForecast, ForecastPeriod

def fake_point_response():
    return {
        "properties": {
            "forecast": "https://api.weather.gov/gridpoints/XXX/0,0/forecast"
        }
    }

def fake_forecast_response():
    # Return at least 6 periods (3 days)
    return {
        "properties": {
            "periods": [
                {
                    "name": f"Period {i}",
                    "temperature": 70 + i,
                    "temperatureUnit": "F",
                    "shortForecast": "Sunny",
                }
                for i in range(6)
            ]
        }
    }

@patch("polaris.weather.client.requests.get")
def test_three_day_forecast(mock_get):
    # Mock two sequential GET calls
    mock_get.side_effect = [
        DummyResp(fake_point_response()),
        DummyResp(fake_forecast_response()),
    ]

    client = ForecastClient(35.0, -97.0)
    result = client.get_three_day_forecast()

    assert isinstance(result, ThreeDayForecast)
    assert len(result.periods) == 6
    assert isinstance(result.periods[0], ForecastPeriod)


class DummyResp:
    """Simple helper class for mocked responses."""
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

    def raise_for_status(self):
        return