import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        print("Testing POST /api/v1/auth/register...")
        resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "tester@example.com", "password": "SuperStrongPassword123!"}
        )
        print("Status:", resp.status_code)
        print("Response:", resp.json())
        
        print("\nTesting POST /api/v1/auth/login...")
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "tester@example.com", "password": "SuperStrongPassword123!"}
        )
        print("Status:", resp.status_code)
        print("Response:", resp.json())
        if resp.status_code != 200:
            return
            
        data = resp.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        
        print("\nTesting GET /api/v1/auth/me...")
        resp = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print("Status:", resp.status_code)
        print("Response:", resp.json())
        
        print("\nTesting POST /api/v1/auth/refresh...")
        resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        print("Status:", resp.status_code)
        print("Response:", resp.json())
        if resp.status_code != 200:
            return
            
        new_refresh = resp.json()["refresh_token"]
        
        print("\nTesting POST /api/v1/auth/refresh (Replay Attack Protection)...")
        resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        print("Status:", resp.status_code)
        print("Response:", resp.json())
        
        print("\nTesting POST /api/v1/auth/logout...")
        resp = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": new_refresh}
        )
        print("Status:", resp.status_code)
        print("Response:", resp.json())

if __name__ == "__main__":
    asyncio.run(main())
