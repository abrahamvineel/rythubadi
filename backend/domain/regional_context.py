from dataclasses import dataclass

@dataclass(frozen=True)
class RegionalContext:
    province_state: str