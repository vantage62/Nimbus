import pytest
import uuid
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def auth_headers(client: AsyncClient, test_user_payload: dict):
    await client.post("/api/v1/auth/register", json=test_user_payload)
    resp = await client.post("/api/v1/auth/login", json=test_user_payload)
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def business_context(client: AsyncClient, auth_headers: dict):
    uid = str(uuid.uuid4())[:8]
    data = {"name": f"Test Business {uid}", "slug": f"test-business-{uid}"}
    resp = await client.post("/api/v1/business/", json=data, headers=auth_headers)
    assert resp.status_code == 201
    business_id = resp.json()["id"]
    return {"business_id": business_id, "headers": auth_headers | {"x-business-id": business_id}}

async def test_create_business(client: AsyncClient, auth_headers: dict):
    uid = str(uuid.uuid4())[:8]
    data = {"name": f"My Business {uid}", "slug": f"my-business-{uid}"}
    resp = await client.post("/api/v1/business/", json=data, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["name"] == data["name"]

async def test_create_category(client: AsyncClient, business_context: dict):
    headers = business_context["headers"]
    resp = await client.post("/api/v1/categories/", json={"name": "Electronics"}, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Electronics"

async def test_create_product(client: AsyncClient, business_context: dict):
    headers = business_context["headers"]
    
    # Create category and supplier first
    cat_resp = await client.post("/api/v1/categories/", json={"name": "Tech"}, headers=headers)
    cat_id = cat_resp.json()["id"]
    
    sup_resp = await client.post("/api/v1/suppliers/", json={"name": "Acme Corp"}, headers=headers)
    sup_id = sup_resp.json()["id"]
    
    uid = str(uuid.uuid4())[:8]
    prod_data = {
        "sku": f"SKU-{uid}",
        "name": "Laptop",
        "cost_price": 500.0,
        "selling_price": 999.99,
        "category_id": cat_id,
        "supplier_id": sup_id
    }
    prod_resp = await client.post("/api/v1/products/", json=prod_data, headers=headers)
    assert prod_resp.status_code == 201
    assert prod_resp.json()["sku"] == prod_data["sku"]

    # Duplicate SKU test
    duplicate_prod = await client.post("/api/v1/products/", json=prod_data, headers=headers)
    assert duplicate_prod.status_code == 409
