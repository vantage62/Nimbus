from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from app.database.base import Base, SoftDeleteMixin
from datetime import datetime

class User(Base, SoftDeleteMixin):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_token: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    verification_token_expires_at: Mapped[datetime | None]
    
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    memberships: Mapped[list["BusinessMembership"]] = relationship("BusinessMembership", back_populates="user")
    roles: Mapped[list["Role"]] = relationship("Role", secondary="user_roles", back_populates="users")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    hashed_token: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    expires_at: Mapped[datetime]
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

class Role(Base):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))
    
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary="role_permissions")
    users: Mapped[list["User"]] = relationship("User", secondary="user_roles", back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"
    name: Mapped[str] = mapped_column(String(100), unique=True)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True)
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True)
)
