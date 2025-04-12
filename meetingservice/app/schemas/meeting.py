from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

class CreateMeetingSchema(BaseModel):
    name: str
    discription: str
    date: datetime


class UpdateMeetingSchema(BaseModel):
    name: str = Field(default=None)
    discription: str = Field(default=None)
    date: datetime = Field(default=None)


class AddUserSchema(BaseModel):
    email: EmailStr
    user_id: UUID