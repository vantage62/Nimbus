import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.modules.auth.crud import (
    get_user_by_email, create_user, store_refresh_token, 
    get_refresh_token, revoke_refresh_token
)
from app.core.exceptions.base import NimbusException
from app.core.security import (
    verify_password, create_access_token, create_refresh_token, decode_token
)
import hashlib

def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def register(session: AsyncSession, user_in: RegisterRequest):
    existing_user = await get_user_by_email(session, user_in.email)
    if existing_user:
        raise NimbusException(status_code=409, message="Email already registered", code="EMAIL_IN_USE")
    
    verification_token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).replace(tzinfo=None)
    
    user = await create_user(session, user_in, verification_token, expires_at)
    return user

async def login(session: AsyncSession, login_in: LoginRequest) -> TokenResponse:
    user = await get_user_by_email(session, login_in.email)
    if not user:
        raise NimbusException(status_code=401, message="Incorrect email or password", code="UNAUTHORIZED")
    
    if not verify_password(login_in.password, user.hashed_password):
        raise NimbusException(status_code=401, message="Incorrect email or password", code="UNAUTHORIZED")
        
    if not user.is_active:
        raise NimbusException(status_code=403, message="Inactive user", code="INACTIVE_USER")
    
    # Generate random jti for tokens
    jti = secrets.token_hex(16)
    
    # Note: active_business_id is omitted at login; the client can switch business contexts later
    access_token = create_access_token(subject=str(user.id), jti=jti)
    refresh_token_plain, expires_at = create_refresh_token(subject=str(user.id), jti=jti)
    
    # Store hashed refresh token
    await store_refresh_token(
        session, str(user.id), _hash_token(refresh_token_plain), expires_at
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_plain,
        token_type="bearer"
    )

async def refresh_tokens(session: AsyncSession, request: RefreshRequest) -> TokenResponse:
    hashed = _hash_token(request.refresh_token)
    stored_token = await get_refresh_token(session, hashed)
    
    if not stored_token:
        raise NimbusException(status_code=401, message="Invalid refresh token", code="UNAUTHORIZED")
        
    if stored_token.revoked:
        # Replay attack detected. Revoke ALL tokens for this user ideally, but for now we just deny.
        raise NimbusException(status_code=401, message="Token has been revoked", code="TOKEN_REVOKED")
        
    if stored_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        raise NimbusException(status_code=401, message="Token expired", code="TOKEN_EXPIRED")
        
    # Valid token. Revoke it immediately to rotate.
    await revoke_refresh_token(session, str(stored_token.id))
    
    # Decode to get user_id (subject)
    try:
        payload = decode_token(request.refresh_token)
        user_id = payload.get("sub")
    except Exception:
        raise NimbusException(status_code=401, message="Invalid token payload", code="UNAUTHORIZED")
        
    jti = secrets.token_hex(16)
    access_token = create_access_token(subject=user_id, jti=jti)
    new_refresh_token, expires_at = create_refresh_token(subject=user_id, jti=jti)
    
    await store_refresh_token(
        session, user_id, _hash_token(new_refresh_token), expires_at
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

async def logout(session: AsyncSession, refresh_token: str) -> None:
    hashed = _hash_token(refresh_token)
    stored_token = await get_refresh_token(session, hashed)
    if stored_token and not stored_token.revoked:
        await revoke_refresh_token(session, str(stored_token.id))
