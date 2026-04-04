from typing import Protocol

class ISoilMoistureProvider(Protocol):

    def get_soil_moisture(self, province_state: str) -> float: ...
