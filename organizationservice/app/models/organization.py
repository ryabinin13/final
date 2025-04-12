from typing import Optional
from sqlalchemy import Date, ForeignKey, Integer, Sequence, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date
import uuid


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    team_id: Mapped[uuid.UUID]
    parent_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=True)

