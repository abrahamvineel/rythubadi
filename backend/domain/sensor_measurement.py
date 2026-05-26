from dataclasses import dataclass
from domain.sensor_type import SensorType
import math

@dataclass(frozen=True)
class SensorMeasurement:
    sensor_type: SensorType
    value: float
    unit: str

    def __post_init__(self):
        if not math.isfinite(self.value):
            raise ValueError("Value is infinite")