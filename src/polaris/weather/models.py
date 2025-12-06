from dataclasses import dataclass
from typing import List

@dataclass
class ForecastPeriod:
    name: str
    temperature: int
    temperature_unit: str
    short_forecast: str

@dataclass
class ThreeDayForecast:
    periods: List[ForecastPeriod]