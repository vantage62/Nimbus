from sqlalchemy import String, ForeignKey, CheckConstraint, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin, VersionedMixin
from decimal import Decimal

class Product(Base, SoftDeleteMixin, VersionedMixin):
    __tablename__ = "products"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    category_id: Mapped[UUID | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    supplier_id: Mapped[UUID | None] = mapped_column(ForeignKey("suppliers.id", ondelete="SET NULL"))
    
    sku: Mapped[str] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(255))
    cost_price: Mapped[Decimal] = mapped_column(Numeric(12, 4), default=Decimal('0.0'))
    selling_price: Mapped[Decimal] = mapped_column(Numeric(12, 4), default=Decimal('0.0'))
    
    minimum_stock: Mapped[int] = mapped_column(default=0)
    safety_stock: Mapped[int] = mapped_column(default=0)
    reorder_point: Mapped[int] = mapped_column(default=0)
    
    __table_args__ = (
        CheckConstraint("cost_price >= 0", name="chk_product_cost_price"),
        CheckConstraint("selling_price >= 0", name="chk_product_selling_price"),
        CheckConstraint("minimum_stock >= 0", name="chk_product_minimum_stock"),
        CheckConstraint("safety_stock >= 0", name="chk_product_safety_stock"),
        CheckConstraint("reorder_point >= 0", name="chk_product_reorder_point"),
        Index("ix_product_business_category", "business_id", "category_id", postgresql_where="deleted_at IS NULL"),
        Index("ix_product_business_sku", "business_id", "sku", unique=True, postgresql_where="deleted_at IS NULL")
    )
