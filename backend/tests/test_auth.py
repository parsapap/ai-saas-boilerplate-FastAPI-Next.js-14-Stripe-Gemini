import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_endpoint_exists(client: AsyncClient):
    """Test that login endpoint is accessible"""
    # Test login endpoint exists (should return 401 for invalid credentials)
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrong"
        }
    )
    # Should return 401 (unauthorized) or 422 (validation error), not 404
    assert response.status_code in [401, 422]
    assert response.status_code != 404
