import pytest
import time
from infrastructure.circuit_breaker import CircuitBreaker, CircuitOpenError


def _always_fail(x: str) -> float:
    raise ConnectionError("provider down")


def _always_succeed(x: str) -> float:
    return 42.0


class TestCircuitBreaker:

    def test_passes_through_on_success(self):
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0)
        result = cb.call(_always_succeed, "ontario")
        assert result == 42.0

    def test_opens_after_threshold_failures(self):
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0)
        for _ in range(3):
            with pytest.raises(ConnectionError):
                cb.call(_always_fail, "ontario")
        # Circuit is now open — next call must be blocked immediately
        with pytest.raises(CircuitOpenError):
            cb.call(_always_fail, "ontario")

    def test_resets_failure_count_on_success(self):
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0)
        # Two failures, then success — count resets
        with pytest.raises(ConnectionError):
            cb.call(_always_fail, "ontario")
        with pytest.raises(ConnectionError):
            cb.call(_always_fail, "ontario")
        cb.call(_always_succeed, "ontario")
        # Two more failures — still below threshold, circuit stays closed
        with pytest.raises(ConnectionError):
            cb.call(_always_fail, "ontario")
        with pytest.raises(ConnectionError):
            cb.call(_always_fail, "ontario")
        # Should NOT raise CircuitOpenError — only 2 consecutive failures
        with pytest.raises(ConnectionError):
            cb.call(_always_fail, "ontario")

    def test_half_opens_after_recovery_timeout(self, monkeypatch):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1.0)
        for _ in range(2):
            with pytest.raises(ConnectionError):
                cb.call(_always_fail, "ontario")
        with pytest.raises(CircuitOpenError):
            cb.call(_always_fail, "ontario")

        # Simulate recovery timeout elapsed — capture real value before patching
        real_now = time.monotonic()
        monkeypatch.setattr(time, "monotonic", lambda: real_now + 2.0)

        # Half-open: one probe allowed through
        result = cb.call(_always_succeed, "ontario")
        assert result == 42.0
        # Circuit closed again — should pass through normally
        assert cb.call(_always_succeed, "ontario") == 42.0
