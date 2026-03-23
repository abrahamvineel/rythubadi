from enum import Enum, auto
from datetime import timedelta

class PerishabilityLevel(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    
    def to_timedelta(self):
        if self == PerishabilityLevel.CRITICAL:
            return timedelta(hours=6)
        elif self == PerishabilityLevel.HIGH:
            return timedelta(hours=48)
        elif self == PerishabilityLevel.MEDIUM:
            return timedelta(days=7)
        elif self == PerishabilityLevel.LOW:
            return timedelta(days=120)
        