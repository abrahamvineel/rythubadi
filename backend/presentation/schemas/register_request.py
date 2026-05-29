from pydantic import BaseModel, model_validator
from typing import Optional

class RegisterRequest(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    name: str
    password: str
    language: str = "EN"
    province_state: str = "general"
    country: str = "CA"
    producer_types: list[str] = []

    @model_validator(mode="after")
    def validate_fields(self):
        if self.email is None and self.phone_number is None:
            raise ValueError("At least one of email or phone_number is required")
        if not self.producer_types:
            raise ValueError("At least one producer type is required")
        return self
