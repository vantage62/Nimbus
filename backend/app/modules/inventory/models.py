from sqlalchemy import ForeignKey, CheckConstraint, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin, VersionedMixin
from datetime import datetime

class Inventory(Base, SoftDeleteMixin, VersionedMixin):
    __tablename__ = "inventory"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    store_id: Mapped[UUID | None] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    
    quantity: Mapped[int] = mapped_column(default=0)
    reserved_quantity: Mapped[int] = mapped_column(default=0)
    available_quantity: Mapped[int] = mapped_column(default=0)
    
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="chk_inventory_quantity"),
        CheckConstraint("reserved_quantity >= 0", name="chk_inventory_reserved"),
        CheckConstraint("available_quantity >= 0", name="chk_inventory_available"),
        Index("ix_inventory_business_product", "business_id", "product_id", "store_id"),
    )

class StockMovement(Base):
    __tablename__ = "stock_movements"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    store_id: Mapped[UUID | None] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    
    movement_type: Mapped[str] = mapped_column(String(50)) # Initial Stock, Purchase, Sale, Return, Damage, Manual Adjustment, Restock, Transfer
    quantity_change: Mapped[int]
    notes: Mapped[str | None] = mapped_column(String(512))
    
    __table_args__ = (
        Index("ix_stock_movement_business_product", "business_id", "product_id", "created_at"),
    )
