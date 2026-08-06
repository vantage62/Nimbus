import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker



# Since we want to use the actual running Postgres DB for integration testing 
# without wiping it, we will use the same DATABASE_URL but we will wrap each
# test in a transaction and rollback, or just allow side effects if requested.
# However, for true integration testing, side-effects are often left if we don't wipe.
# Given the user specifically requested "The PostgreSQL volume should remain intact", 
# we will just interact with the live DB.

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

# Test Data Generators
@pytest.fixture
def test_user_payload():
    import uuid
    uid = str(uuid.uuid4())[:8]
    return {
        "email": f"testuser_{uid}@example.com",
        "password": "StrongPassword123!"
    }
