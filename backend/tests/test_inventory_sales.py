import pytest
import uuid
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def auth_headers(client: AsyncClient):
    uid = str(uuid.uuid4())[:8]
    payload = {"email": f"test_{uid}@example.com", "password": "StrongPassword123"}
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/login", json=payload)
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

@pytest.fixture
async def setup_data(client: AsyncClient, auth_headers: dict):
    uid = str(uuid.uuid4())[:8]
    b_resp = await client.post("/api/v1/business/", json={"name": f"Biz {uid}", "slug": f"biz-{uid}"}, headers=auth_headers)
    b_id = b_resp.json()["id"]
    headers = auth_headers | {"x-business-id": b_id}
    
    p_resp = await client.post("/api/v1/products/", json={"sku": f"SKU-{uid}", "name": "Item"}, headers=headers)
    p_id = p_resp.json()["id"]
    
    return {"business_id": b_id, "headers": headers, "product_id": p_id}

async def test_inventory_adjustment(client: AsyncClient, setup_data: dict):
    headers = setup_data["headers"]
    product_id = setup_data["product_id"]
    
    adj_data = {
        "product_id": product_id,
        "movement_type": "Initial Stock",
        "quantity_change": 50,
        "notes": "Testing"
    }
    
    resp = await client.post("/api/v1/inventory/adjust", json=adj_data, headers=headers)
    assert resp.status_code == 201
    
    # Check inventory
    inv_list = await client.get("/api/v1/inventory/", headers=headers)
    print("INV LIST JSON:", inv_list.json())
    assert inv_list.json()["total"] >= 1
    
    items = inv_list.json()["items"]
    prod_inv = next(i for i in items if i["product_id"] == product_id)
    assert prod_inv["quantity"] == 50

async def test_negative_inventory_rejection(client: AsyncClient, setup_data: dict):
    headers = setup_data["headers"]
    product_id = setup_data["product_id"]
    
    # Attempt to deduct from empty stock
    adj_data = {
        "product_id": product_id,
        "movement_type": "Damage",
        "quantity_change": -10,
    }
    resp = await client.post("/api/v1/inventory/adjust", json=adj_data, headers=headers)
    assert resp.status_code == 400
    assert "Cannot deduct stock" in resp.json()["message"]

async def test_sale_creation(client: AsyncClient, setup_data: dict):
    headers = setup_data["headers"]
    product_id = setup_data["product_id"]
    
    # Add stock first
    await client.post("/api/v1/inventory/adjust", json={
        "product_id": product_id,
        "movement_type": "Initial Stock",
        "quantity_change": 10
    }, headers=headers)
    
    # Create Sale
    sale_data = {
        "product_id": product_id,
        "quantity": 3,
        "unit_price": 25.0
    }
    resp = await client.post("/api/v1/sales/", json=sale_data, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["total_amount"] == "75.0000"
    
    # Verify stock deducted
    inv_list = await client.get("/api/v1/inventory/", headers=headers)
    prod_inv = next(i for i in inv_list.json()["items"] if i["product_id"] == product_id)
    assert prod_inv["quantity"] == 7
