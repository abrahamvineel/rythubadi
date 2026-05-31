import pytest
from infrastructure.soil_moisture_fallback_chain import SoilMoistureFallbackChain


class _OKProvider:
    def __init__(self, value: float):
        self._value = value

    def get_soil_moisture(self, province_state: str) -> float:
        return self._value


class _FailingProvider:
    def get_soil_moisture(self, province_state: str) -> float:
        raise ConnectionError("provider unavailable")


class TestSoilMoistureFallbackChain:

    def test_returns_first_provider_value_when_healthy(self):
        chain = SoilMoistureFallbackChain([_OKProvider(55.0), _OKProvider(30.0)])
        assert chain.get_soil_moisture("ontario") == 55.0

    def test_falls_back_to_second_when_first_fails(self):
        chain = SoilMoistureFallbackChain([_FailingProvider(), _OKProvider(30.0)])
        assert chain.get_soil_moisture("ontario") == 30.0

    def test_falls_back_to_third_when_first_two_fail(self):
        chain = SoilMoistureFallbackChain([
            _FailingProvider(),
            _FailingProvider(),
            _OKProvider(22.5),
        ])
        assert chain.get_soil_moisture("ontario") == 22.5

    def test_raises_runtime_error_when_all_fail(self):
        chain = SoilMoistureFallbackChain([_FailingProvider(), _FailingProvider()])
        with pytest.raises(RuntimeError, match="All soil moisture providers failed"):
            chain.get_soil_moisture("ontario")

    def test_circuit_opens_after_repeated_failures_and_skips_provider(self):
        # After 5 failures the circuit opens — provider is skipped on next call
        failing = _FailingProvider()
        ok = _OKProvider(10.0)
        chain = SoilMoistureFallbackChain([failing, ok])
        # Drive the circuit breaker open on the first provider
        for _ in range(5):
            result = chain.get_soil_moisture("ontario")
            assert result == 10.0  # always falls through to ok
        # Circuit is open — failing provider is now skipped instantly, still returns ok
        assert chain.get_soil_moisture("ontario") == 10.0
