from pydantic import BaseModel, field_validator

class AddProducerTypesRequest(BaseModel):
    producer_types: list[str]

    @field_validator("producer_types")
    @classmethod
    def must_not_be_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("producer_types must contain at least one type")
        return v
