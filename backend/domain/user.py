from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from domain.exceptions import NoContactMethodError
from domain.language import Language
from domain.regional_context import RegionalContext

@dataclass(frozen=True)
class User:
    id: UUID
    email: Optional[str]
    phone_number: Optional[str]
    name: str
    password_hash: str
    language: Language
    province_state: RegionalContext

    def __post_init__(self):
        if self.email is None and self.phone_number is None:
            raise NoContactMethodError("Email or phone number is not present")
        