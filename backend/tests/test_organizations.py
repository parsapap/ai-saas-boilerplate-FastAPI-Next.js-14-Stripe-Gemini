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
async def test_create_organization(client: AsyncClient, test_user_data, test_org_data):
    """Test creating an organization"""
    token = await get_auth_token(client, test_user_data)
    
    response = await client.post(
        "/api/v1/orgs/",
        json=test_org_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_org_data["name"]
    assert data["slug"] == test_org_data["slug"]
    assert "id" in data


@pytest.mark.asyncio
async def test_list_organizations(client: AsyncClient, test_user_data, test_org_data):
    """Test listing organizations"""
    token = await get_auth_token(client, test_user_data)
    
    # Create an organization
    await client.post(
        "/api/v1/orgs/",
        json=test_org_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # List organizations
    response = await client.get(
        "/api/v1/orgs/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == test_org_data["name"]


@pytest.mark.asyncio
async def test_get_organization(client: AsyncClient, test_user_data, test_org_data):
    """Test getting a specific organization"""
    token = await get_auth_token(client, test_user_data)
    
    # Create an organization
    create_response = await client.post(
        "/api/v1/orgs/",
        json=test_org_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    org_id = create_response.json()["id"]
    
    # Get the organization
    response = await client.get(
        f"/api/v1/orgs/{org_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == org_id
    assert data["name"] == test_org_data["name"]
