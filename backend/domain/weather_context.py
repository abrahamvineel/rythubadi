from dataclasses import dataclass
from domain.data_precision import DataPrecision
from typing import Optional
from domain.exceptions import InvalidHumidityRange, InvalidTemperatureCelciusRange, InvalidPrecipitationValue, InvalidLowTemperature
@dataclass(frozen=True)
class WeatherContext:
    temperature: float
    high_temperature: float
    low_temperature: float
    uv_index: Optional[int]
    wind: Optional[float]
    precipitation: float
    visibility: Optional[float]
    pressure: Optional[float]
    humidity: float
    precision_level: DataPrecision

    def __post_init__(self):
        if (self.temperature < -80 or self.temperature > 80) \
           or (self.low_temperature < -80 or self.high_temperature > 80):
            raise InvalidTemperatureCelciusRange("Temperature in celcius should be in range of -80 to 80")
        if self.humidity < 0 or self.humidity > 100:
            raise InvalidHumidityRange("Humidity should be in range 0 to 100")
        if self.precipitation < 0:
            raise InvalidPrecipitationValue("Precipitation should be greater than zero")
        if self.low_temperature > self.high_temperature:
            raise InvalidLowTemperature("Low temperature should be lesser than high temperature")