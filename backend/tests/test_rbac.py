import pytest
import uuid
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def multi_users(client: AsyncClient):
    users = {}
    for role in ["owner", "admin", "manager", "employee"]:
        uid = str(uuid.uuid4())[:8]
        payload = {"email": f"{role}_{uid}@example.com", "password": "StrongPassword123"}
        await client.post("/api/v1/auth/register", json=payload)
        resp = await client.post("/api/v1/auth/login", json=payload)
        users[role] = {
            "token": resp.json()["access_token"],
            "headers": {"Authorization": f"Bearer {resp.json()['access_token']}"},
            "id": uid
        }
    return users

async def test_tenant_isolation(client: AsyncClient, multi_users: dict):
    # Owner 1 creates a business
    owner1_h = multi_users["owner"]["headers"]
    b_resp = await client.post("/api/v1/business/", json={"name": "Biz 1", "slug": f"biz-{multi_users['owner']['id']}"}, headers=owner1_h)
    b_id = b_resp.json()["id"]
    
    # Another user tries to access that business without membership
    owner2_h = multi_users["admin"]["headers"]
    
    # Note: Since auth logic currently resolves 'x-business-id' by checking current_user.memberships in `get_current_business`
    # Let's test providing the foreign business ID
    resp = await client.get(f"/api/v1/business/{b_id}", headers=owner2_h | {"x-business-id": b_id})
    assert resp.status_code in [403, 401] # Depends on exact exception raised by get_current_business
