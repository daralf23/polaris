from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ForecastPeriod:
    name: str
    temperature: int
    temperature_unit: str
    short_forecast: str
    detailed_forecast: str
    wind_speed: str
    wind_direction: str


@dataclass(slots=True)
class WeatherForecast:
    periods: list[ForecastPeriod]
