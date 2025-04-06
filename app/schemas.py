from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IterationCreate(BaseModel):
    name: str
    description: str


class IterationResponse(IterationCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
