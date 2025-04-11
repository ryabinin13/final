from ..database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Event(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[uuid.UUID]
    title: Mapped[str]
    discription: Mapped[str]