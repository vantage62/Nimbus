from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin

class Category(Base, SoftDeleteMixin):
    __tablename__ = "categories"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(512))
    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    
    __table_args__ = (
        Index("ix_category_business_name", "business_id", "name"),
    )
