from pydantic import BaseModel, Field


class CreateTaskSchema(BaseModel):

    title: str
    discription: str


class UpdateTaskSchema(BaseModel):

    title: str = Field(default=None)
    discription: str = Field(default=None)
    status: str = Field(default=None)