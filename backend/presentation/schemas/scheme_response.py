from pydantic import BaseModel, Field
from domain.language import Language
from uuid import UUID

class SchemeResponse(BaseModel):
    response: str
    tools_called: list[str]
    