import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, user_data):
    """Helper to get auth token"""
    await client.post("/api/v1/auth/register", json=user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    return login_response.json()["access_token"]


@pytest.mark.asyncio
async def test_get_plans(client: AsyncClient):
    """Test getting available plans"""
    response = await client.get("/api/v1/billing/plans")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # Free, Pro, Team
    
    # Check plan structure
    for plan in data:
        assert "name" in plan
        assert "type" in plan
        assert "price" in plan
        assert "features" in plan


@pytest.mark.asyncio
async def test_get_subscription(client: AsyncClient, test_user_data, test_org_data):
    """Test getting current subscription"""
    token = await get_auth_token(client, test_user_data)
    
    # Create organization
    org_response = await client.post(
        "/api/v1/orgs/",
        json=test_org_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    org_id = org_response.json()["id"]
    
    # Get subscription
    response = await client.get(
        "/api/v1/billing/subscription",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Current-Org": str(org_id)
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["plan_type"] == "free"  # Default plan
