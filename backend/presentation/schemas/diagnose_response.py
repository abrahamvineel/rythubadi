from uuid import UUID
from pydantic import BaseModel

class DiagnoseResponse(BaseModel):
    llm_diagnosis: str
    pending_confirmation: bool = True
    confirmation_id: UUID
