import enum
from sqlalchemy import Enum
from app.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class MeetingMemberships(Base):
    
    __tablename__ = "meeting_memberships"

    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int]
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
