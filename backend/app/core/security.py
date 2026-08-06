from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from authlib.jose import jwt
from app.core.config import settings

ph = PasswordHasher()

def get_password_hash(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False

def create_access_token(
    subject: str,
    active_business_id: str | None = None,
    jti: str | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    header = {"alg": settings.JWT_ALGORITHM}
    payload = {
        "sub": subject,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    
    if active_business_id:
        payload["active_business_id"] = active_business_id
    if jti:
        payload["jti"] = jti
        
    return jwt.encode(header, payload, settings.JWT_SECRET_KEY).decode("utf-8")

def create_refresh_token(subject: str, jti: str) -> tuple[str, datetime]:
    now = datetime.now(timezone.utc)
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    expires_at = (now + expires_delta).replace(tzinfo=None)
    
    header = {"alg": settings.JWT_ALGORITHM}
    payload = {
        "sub": subject,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": jti,
    }
    
    token = jwt.encode(header, payload, settings.JWT_SECRET_KEY).decode("utf-8")
    return token, expires_at

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY)
