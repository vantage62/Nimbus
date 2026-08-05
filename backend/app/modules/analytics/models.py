from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID
from app.database.base import Base
from datetime import datetime

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    snapshot_date: Mapped[datetime]
    metric_name: Mapped[str] = mapped_column(String(255))
    value: Mapped[dict] = mapped_column(JSONB)
