from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin

class Supplier(Base, SoftDeleteMixin):
    __tablename__ = "suppliers"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    contact_email: Mapped[str | None] = mapped_column(String(255))
    lead_time_days: Mapped[int] = mapped_column(default=0)
    
    __table_args__ = (
        CheckConstraint("lead_time_days >= 0", name="chk_supplier_lead_time"),
    )
