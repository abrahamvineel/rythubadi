from pydantic import BaseModel
from typing import Optional

class CreateMessageRequest(BaseModel):
    content: str
    attachment_url: Optional[str] = None
    system_generated: bool = False
    language: str = "EN"
