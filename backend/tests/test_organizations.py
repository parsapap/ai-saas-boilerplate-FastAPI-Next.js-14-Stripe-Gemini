import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_organization_endpoints_exist(client: AsyncClient):
    """Test that organization endpoints are accessible"""
    # Test list endpoint exists (should require auth)
    response = await client.get("/api/v1/orgs/")
    # Should return 401 (unauthorized) or 307 (redirect), not 404
    assert response.status_code != 404
