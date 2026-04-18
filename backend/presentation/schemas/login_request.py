from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: str
    