from pydantic import BaseModel


class CreateMarkSchema(BaseModel):

    task_id: int
    mark: int   