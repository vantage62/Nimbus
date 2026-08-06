from typing import Annotated, Callable
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.session import get_db
from app.modules.auth.models import User, Role
from app.modules.auth.crud import get_user_by_id
from app.core.security import decode_token
from app.core.exceptions.base import NimbusException
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise NimbusException(status_code=401, message="Could not validate credentials", code="UNAUTHORIZED")
    except Exception:
        raise NimbusException(status_code=401, message="Could not validate credentials", code="UNAUTHORIZED")
        
    # We must eagerly load roles, permissions, and memberships so RBAC works efficiently
    # For a real scalable app, we might cache this in Redis.
    from sqlalchemy import select
    stmt = (
        select(User)
        .options(
            selectinload(User.roles).selectinload(Role.permissions),
            selectinload(User.memberships)
        )
        .where(User.id == UUID(user_id))
    )
    result = await session.execute(stmt)
    user = result.scalars().first()
    
    if user is None:
        raise NimbusException(status_code=401, message="User not found", code="USER_NOT_FOUND")
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise NimbusException(status_code=403, message="Inactive user", code="INACTIVE_USER")
    return current_user

def require_role(role_name: str) -> Callable:
    async def role_checker(user: Annotated[User, Depends(get_current_active_user)]) -> User:
        user_roles = [r.name for r in user.roles]
        if role_name not in user_roles and "superuser" not in user_roles:
            raise NimbusException(status_code=403, message=f"Role {role_name} required", code="FORBIDDEN")
        return user
    return role_checker

def require_permission(permission_name: str) -> Callable:
    async def permission_checker(user: Annotated[User, Depends(get_current_active_user)]) -> User:
        user_permissions = {p.name for role in user.roles for p in role.permissions}
        user_roles = [r.name for r in user.roles]
        if permission_name not in user_permissions and "superuser" not in user_roles:
            raise NimbusException(status_code=403, message=f"Permission {permission_name} required", code="FORBIDDEN")
        return user
    return permission_checker

async def get_current_business(
    business_id: UUID,
    user: Annotated[User, Depends(get_current_active_user)]
) -> UUID:
    user_roles = [r.name for r in user.roles]
    if "superuser" in user_roles:
        return business_id
        
    for membership in user.memberships:
        if membership.business_id == business_id:
            return business_id
            
    raise NimbusException(status_code=403, message="Not a member of this business", code="FORBIDDEN")
