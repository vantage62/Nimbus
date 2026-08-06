import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(default=None, index=True)

class VersionedMixin:
    version: Mapped[int] = mapped_column(default=1, nullable=False, server_default="1")
    __mapper_args__ = {"version_id_col": version}
