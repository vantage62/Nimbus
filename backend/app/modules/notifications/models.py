from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin

class Notification(Base, SoftDeleteMixin):
    __tablename__ = "notifications"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    business_id: Mapped[UUID | None] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
