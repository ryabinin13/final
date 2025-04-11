from typing import Optional
from sqlalchemy import Date, Integer, Sequence, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date
import uuid


class OrganizationMembership(Base):
    __tablename__ = "organizations_membership"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    