from pydantic import BaseModel
from typing import Optional

class ChatResponse(BaseModel):
    specialist_response: str
    routed_to: str
    