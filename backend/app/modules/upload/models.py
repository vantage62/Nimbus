from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.database.base import Base

class CsvUpload(Base):
    __tablename__ = "csv_uploads"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    
    filename: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    rows_processed: Mapped[int] = mapped_column(Integer, default=0)
    error_log: Mapped[str | None]
