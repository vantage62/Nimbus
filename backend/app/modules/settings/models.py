from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID
from app.database.base import Base, VersionedMixin

class Setting(Base, VersionedMixin):
    __tablename__ = "settings"
    business_id: Mapped[UUID | None] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    key: Mapped[str] = mapped_column(String(255))
    value: Mapped[dict] = mapped_column(JSONB)
    
    __table_args__ = (
        Index("ix_setting_business_key", "business_id", "key", unique=True),
    )
