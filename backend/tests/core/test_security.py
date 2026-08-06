import pytest
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token, decode_token
)
from datetime import datetime, timezone
import time

def test_password_hashing():
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123!", hashed) is False

def test_access_token():
    subject = "123e4567-e89b-12d3-a456-426614174000"
    business_id = "987fcdeb-51a2-43d7-9012-3456789abcde"
    jti = "random-jti"
    
    token = create_access_token(subject=subject, active_business_id=business_id, jti=jti)
    assert token is not None
    
    payload = decode_token(token)
    assert payload["sub"] == subject
    assert payload["type"] == "access"
    assert payload["active_business_id"] == business_id
    assert payload["jti"] == jti
    assert "exp" in payload
    assert "iat" in payload

def test_refresh_token():
    subject = "123e4567-e89b-12d3-a456-426614174000"
    jti = "random-jti"
    
    token, expires_at = create_refresh_token(subject=subject, jti=jti)
    assert token is not None
    assert isinstance(expires_at, datetime)
    
    payload = decode_token(token)
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"
    assert payload["jti"] == jti
    assert "exp" in payload
    assert "iat" in payload
