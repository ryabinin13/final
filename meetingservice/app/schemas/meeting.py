from datetime import datetime
from pydantic import BaseModel, Field

class CreateMeetingSchema(BaseModel):
    name: str
    discription: str
    date: datetime


class UpdateMeetingSchema(BaseModel):
    name: str = Field(default=None)
    discription: str = Field(default=None)
    date: datetime = Field(default=None)