from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID
from sqlalchemy import ForeignKey, String

class AuditLog(Base):
    __tablename__ = "audit_logs"
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(255))
    entity_type: Mapped[str] = mapped_column(String(255))
    entity_id: Mapped[UUID | None]
    changes: Mapped[dict | None] = mapped_column(JSONB)
