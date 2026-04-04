
class FakeSoilMoistureProvider:

    def __init__(self, soil_moisture: float):
        self.soil_moisture = soil_moisture

    def get_soil_moisture(self, province_state: str) -> float:
        return self.soil_moisture
