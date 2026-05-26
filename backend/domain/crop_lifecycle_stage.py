from enum import Enum

class CropLifecycleStage(Enum):
    NURSERY = (55.0, 75.0)
    YOUNG =  (50.0, 70.0)
    PRE_BEARING = (45.0, 68.0)
    BEARING = (40.0, 65.0)
    DECLINING = (40.0, 65.0)

    def moisture_range(self) -> tuple[float, float]:
        return self.value