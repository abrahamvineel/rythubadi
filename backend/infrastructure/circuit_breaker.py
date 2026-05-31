import time


class CircuitOpenError(Exception):
    """Raised when a circuit breaker is open and the call is blocked."""


class CircuitBreaker:
    """
    Wraps a provider callable. After `failure_threshold` consecutive failures,
    the circuit opens for `recovery_timeout` seconds. While open, calls are
    blocked immediately (CircuitOpenError) so a dead upstream does not add
    latency to every request. After the timeout the circuit half-opens: the
    next call is allowed through — if it succeeds the circuit closes, if it
    fails the circuit opens again.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._failure_count = 0
        self._opened_at: float | None = None

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------

    def _is_open(self) -> bool:
        if self._opened_at is None:
            return False
        elapsed = time.monotonic() - self._opened_at
        if elapsed >= self._recovery_timeout:
            # Half-open: allow one probe through
            return False
        return True

    def _record_success(self) -> None:
        self._failure_count = 0
        self._opened_at = None

    def _record_failure(self) -> None:
        self._failure_count += 1
        if self._failure_count >= self._failure_threshold:
            self._opened_at = time.monotonic()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def call(self, fn, *args, **kwargs):
        """
        Execute fn(*args, **kwargs) through the circuit breaker.
        Raises CircuitOpenError if the circuit is open.
        Re-raises the provider exception on failure (and records it).
        """
        if self._is_open():
            raise CircuitOpenError("Circuit is open — provider skipped")
        try:
            result = fn(*args, **kwargs)
            self._record_success()
            return result
        except Exception:
            self._record_failure()
            raise
