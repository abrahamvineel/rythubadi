from dataclasses import dataclass
from datetime import date
import math

@dataclass(frozen=True)
class WeatherForecast:
    forecast_date: date
    precipitation_mm: float
    precipitation_probability_pct: int
    temp_max: float
    temp_min: float

    def __post_init__(self):
        if not math.isfinite(self.precipitation_mm):
            raise ValueError("precipitation_mm must be a finite number")
        if self.precipitation_mm < 0:
            raise ValueError("precipitation_mm cannot be negative")
        if not (0 <= self.precipitation_probability_pct <= 100):
            raise ValueError("precipitation_probability_pct must be between 0 and 100")
        if not math.isfinite(self.temp_max):
            raise ValueError("temp_max must be a finite number")
        if not math.isfinite(self.temp_min):
            raise ValueError("temp_min must be a finite number")
        if self.temp_min > self.temp_max:
            raise ValueError(f"temp_min ({self.temp_min}) cannot exceed temp_max ({self.temp_max})")