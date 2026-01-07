from dataclasses import dataclass


BASE_URL = "https://api.weather.gov"

@dataclass
class ZoneInfo:
    id: str
    name: str
    type: str
    state: str


@dataclass
class ForecastPeriod:
    name: str
    start_time: str
    end_time: str
    temperature: int
    temperature_unit: str
    wind_speed: str
    wind_direction: str
    detailed_forecast: str
