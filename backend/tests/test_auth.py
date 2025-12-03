import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_endpoints_exist(client: AsyncClient):
    """Test that auth endpoints are accessible"""
    # Test register endpoint exists
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "full_name": "Test User"
    })
    # Should return 201 (success) or 400/500 (validation/server error), not 404
    assert response.status_code != 404
    
    # Test login endpoint exists
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    # Should return 401 (unauthorized) or other, not 404
    assert response.status_code != 404
