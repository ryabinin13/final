from typing import Optional
import uuid
from pydantic import BaseModel


class AddOrganizationSchema(BaseModel):
    name: str
    team_id: uuid.UUID
    parent_id: Optional[int] = None
