from sqlalchemy import ForeignKey, CheckConstraint, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin
from decimal import Decimal
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Sale(Base, SoftDeleteMixin):
    __tablename__ = "sales"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    store_id: Mapped[UUID | None] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    
    sale_date: Mapped[datetime] = mapped_column(default=utcnow)
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    discount: Mapped[Decimal] = mapped_column(Numeric(12, 4), default=Decimal('0.0'))
    
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="chk_sale_quantity"),
        Index("ix_sale_business_product_date", "business_id", "product_id", "sale_date"),
    )
