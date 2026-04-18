from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime
from domain.exceptions import NoContactMethodError

@dataclass(frozen=True)
class User:
    id: UUID
    email: Optional[str]
    phone_number: Optional[str]
    name: str
    password_hash: str

    def __post_init__(self):
        if self.email is None and self.phone_number is None:
            raise NoContactMethodError("Email or phone number is not present")
        