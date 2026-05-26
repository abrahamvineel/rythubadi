from dataclasses import dataclass
from uuid import UUID
from domain.producer_type import ProducerType
from datetime import datetime
from domain.data_precision import DataPrecision
from domain.sensor_measurement import SensorMeasurement
from domain.exceptions import SensorReadingTimeZoneError
from domain.sensor_type import SensorType
from typing import Optional

@dataclass(frozen=True)
class SensorReading:
    producer_id: UUID
    producer_type: ProducerType
    measurements: tuple[SensorMeasurement, ...]
    data_precision: DataPrecision
    recorded_at: datetime
    crop_type: Optional[str] = None

    def __post_init__(self):
        if self.recorded_at.tzinfo is None:
            raise SensorReadingTimeZoneError("Sensor timezone reading is none")
    
    def get(self, sensor_type: SensorType) -> Optional[SensorMeasurement]:
        for measurement in self.measurements:
            if measurement.sensor_type == sensor_type:
                return measurement
        return None
    