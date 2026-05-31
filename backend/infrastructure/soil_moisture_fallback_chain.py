import structlog
from infrastructure.circuit_breaker import CircuitBreaker, CircuitOpenError

log = structlog.get_logger()


class SoilMoistureFallbackChain:
    """
    FallbackChain for soil moisture: IoT → NASA SMAP → Open-Meteo.

    Each provider is wrapped in its own CircuitBreaker. On any failure
    (provider exception or open circuit) the chain moves to the next
    provider. If all providers fail, raises RuntimeError.

    Adding a new source = pass it in the providers list. Zero other
    changes required.
    """

    def __init__(self, providers: list):
        # Each entry: (provider, CircuitBreaker)
        self._providers = [
            (provider, CircuitBreaker(failure_threshold=5, recovery_timeout=60.0))
            for provider in providers
        ]

    def get_soil_moisture(self, province_state: str) -> float:
        last_error: Exception | None = None

        for provider, breaker in self._providers:
            name = type(provider).__name__
            try:
                value = breaker.call(provider.get_soil_moisture, province_state)
                log.info("soil_moisture_source", provider=name, province_state=province_state)
                return value
            except CircuitOpenError:
                log.warning("soil_circuit_open", provider=name)
                continue
            except Exception as exc:
                log.warning("soil_provider_failed", provider=name, error=str(exc))
                last_error = exc
                continue

        raise RuntimeError(
            f"All soil moisture providers failed for {province_state!r}. "
            f"Last error: {last_error}"
        )
