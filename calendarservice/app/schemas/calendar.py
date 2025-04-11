from pydantic import BaseModel
from uuid import UUID


class CreateEventSchema(BaseModel):
    team_id: UUID
    title: str
    discription: str