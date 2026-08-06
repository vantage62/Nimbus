import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_register_user(client: AsyncClient, test_user_payload: dict):
    response = await client.post("/api/v1/auth/register", json=test_user_payload)
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == test_user_payload["email"]
    assert "hashed_password" not in data

async def test_register_duplicate_user(client: AsyncClient, test_user_payload: dict):
    # First registration
    await client.post("/api/v1/auth/register", json=test_user_payload)
    # Second registration
    response = await client.post("/api/v1/auth/register", json=test_user_payload)
    assert response.status_code == 409

async def test_login_user(client: AsyncClient, test_user_payload: dict):
    # Register first
    await client.post("/api/v1/auth/register", json=test_user_payload)
    
    # Login
    response = await client.post("/api/v1/auth/login", json=test_user_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

async def test_get_current_user(client: AsyncClient, test_user_payload: dict):
    await client.post("/api/v1/auth/register", json=test_user_payload)
    login_resp = await client.post("/api/v1/auth/login", json=test_user_payload)
    token = login_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = await client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["user"]["email"] == test_user_payload["email"]

async def test_refresh_token(client: AsyncClient, test_user_payload: dict):
    await client.post("/api/v1/auth/register", json=test_user_payload)
    login_resp = await client.post("/api/v1/auth/login", json=test_user_payload)
    refresh_token = login_resp.json()["refresh_token"]
    
    refresh_resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json()
    
    # Replay protection
    replay_resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert replay_resp.status_code == 401

async def test_logout(client: AsyncClient, test_user_payload: dict):
    await client.post("/api/v1/auth/register", json=test_user_payload)
    login_resp = await client.post("/api/v1/auth/login", json=test_user_payload)
    refresh_token = login_resp.json()["refresh_token"]
    
    logout_resp = await client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout_resp.status_code == 200
    
    # Attempt refresh after logout
    refresh_after_logout = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_after_logout.status_code == 401
