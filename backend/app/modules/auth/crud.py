from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.modules.auth.models import User, RefreshToken
from app.modules.auth.schemas import RegisterRequest
from app.core.security import get_password_hash
from datetime import datetime

async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_user_by_id(session: AsyncSession, user_id: str) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def create_user(
    session: AsyncSession, user_in: RegisterRequest, verification_token: str, expires_at: datetime
) -> User:
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        verification_token=verification_token,
        verification_token_expires_at=expires_at,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def store_refresh_token(
    session: AsyncSession, user_id: str, hashed_token: str, expires_at: datetime
) -> RefreshToken:
    token = RefreshToken(
        user_id=user_id,
        hashed_token=hashed_token,
        expires_at=expires_at,
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token

async def get_refresh_token(session: AsyncSession, hashed_token: str) -> Optional[RefreshToken]:
    stmt = select(RefreshToken).where(RefreshToken.hashed_token == hashed_token)
    result = await session.execute(stmt)
    return result.scalars().first()

async def revoke_refresh_token(session: AsyncSession, token_id: str) -> None:
    stmt = select(RefreshToken).where(RefreshToken.id == token_id)
    result = await session.execute(stmt)
    token = result.scalars().first()
    if token:
        token.revoked = True
        session.add(token)
        await session.commit()
