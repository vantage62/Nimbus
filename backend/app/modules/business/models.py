from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin, VersionedMixin

class Business(Base, SoftDeleteMixin, VersionedMixin):
    __tablename__ = "businesses"
    name: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    
    memberships: Mapped[list["BusinessMembership"]] = relationship("BusinessMembership", back_populates="business")
    stores: Mapped[list["Store"]] = relationship("Store", back_populates="business")

class BusinessMembership(Base):
    __tablename__ = "business_memberships"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    role_id: Mapped[UUID | None] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"))
    
    user: Mapped["User"] = relationship("User", back_populates="memberships")
    business: Mapped["Business"] = relationship("Business", back_populates="memberships")
    
    __table_args__ = (
        Index("ix_membership_user_business", "user_id", "business_id", unique=True),
    )

class Store(Base, SoftDeleteMixin):
    __tablename__ = "stores"
    business_id: Mapped[UUID] = mapped_column(ForeignKey("businesses.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(512))
    
    business: Mapped["Business"] = relationship("Business", back_populates="stores")
