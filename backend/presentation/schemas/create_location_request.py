from pydantic import BaseModel, Field


class CreateLocationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    producer_types: list[str] = Field(..., min_length=1)
