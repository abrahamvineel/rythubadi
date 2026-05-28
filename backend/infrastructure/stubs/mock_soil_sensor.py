import random
from uuid import UUID

class MockSoilSensor:

    def read(self, producer_id: UUID) -> float:
        return round(random.uniform(30.0, 75.0), 2)
