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

    @model_validator(mode="after")
    def check_contact_method(self):
        if self.email is None and self.phone_number is None:
            raise ValueError("At least one of email or phone_number is required")
        return self
