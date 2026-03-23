from domain.perishability_level import PerishabilityLevel
from datetime import timedelta

class TestPerishabilityLevel:

    def test_to_timedelta(self):
        assert PerishabilityLevel.CRITICAL.to_timedelta() == timedelta(hours=6)
        assert PerishabilityLevel.HIGH.to_timedelta() == timedelta(hours=48)
        assert PerishabilityLevel.MEDIUM.to_timedelta() == timedelta(days=7)
        assert PerishabilityLevel.LOW.to_timedelta() == timedelta(days=120)
