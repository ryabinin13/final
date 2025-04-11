from pydantic import BaseModel
from app.models.team_memberships import Status


class UserChangeStatusSchema(BaseModel):
    status: Status