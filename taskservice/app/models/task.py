from typing import Optional
from sqlalchemy import Date, Enum, Integer, Sequence, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date
import uuid
import enum

class Status(enum.Enum):
    COMPLETED = "completed"
    ACTIVE = "active"
    INACTIVE = "inactive"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    discription: Mapped[str]
    title: Mapped[str]
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.INACTIVE, nullable=False)
