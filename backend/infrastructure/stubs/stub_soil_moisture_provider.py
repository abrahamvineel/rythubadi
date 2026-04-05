
class StubSoilMoistureProvider:

    def get_soil_moisture(self, province_state: str) -> float:
        return 98.9