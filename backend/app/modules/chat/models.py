from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID
from app.database.base import Base

class AiConversation(Base):
    __tablename__ = "ai_conversations"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    
    title: Mapped[str | None] = mapped_column(String(255))
    messages: Mapped[list[dict]] = mapped_column(JSONB, default=list)
