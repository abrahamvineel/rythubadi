from pydantic import BaseModel
from typing import Optional

class ChatResponse(BaseModel):
    recommendation: str
    data_disclaimer: Optional[str]
    routed_to_agronomist: bool
    