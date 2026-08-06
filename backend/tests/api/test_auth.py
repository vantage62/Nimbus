import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.models import User
from sqlalchemy import select

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db_session: AsyncSession):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "StrongPassword123!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    
    # Verify in DB
    stmt = select(User).where(User.email == "test@example.com")
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    assert user is not None
    assert user.email == "test@example.com"
    assert user.verification_token is not None

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "StrongPassword123!"}
    )
    
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "StrongPassword123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    # Register and Login
    await client.post("/api/v1/auth/register", json={"email": "refresh@example.com", "password": "StrongPassword123!"})
    login_resp = await client.post("/api/v1/auth/login", json={"email": "refresh@example.com", "password": "StrongPassword123!"})
    tokens = login_resp.json()
    old_refresh_token = tokens["refresh_token"]
    
    # Refresh
    refresh_resp = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token}
    )
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    assert new_tokens["refresh_token"] != old_refresh_token
    
    # Try old refresh token (Replay attack)
    bad_resp = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh_token}
    )
    assert bad_resp.status_code == 401

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={"email": "me@example.com", "password": "StrongPassword123!"})
    login_resp = await client.post("/api/v1/auth/login", json={"email": "me@example.com", "password": "StrongPassword123!"})
    tokens = login_resp.json()
    
    me_resp = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert me_resp.status_code == 200
    data = me_resp.json()
    assert data["user"]["email"] == "me@example.com"
