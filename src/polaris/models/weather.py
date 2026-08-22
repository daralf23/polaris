from pydantic import BaseModel


class WeatherConfig(BaseModel):
    latitude: float
    longitude: float

    periods: int = 6

    label: str = "Home"

    normal_poll: str = "*/15 * * * *"
    alert_poll: str = "*/1 * * * *"
