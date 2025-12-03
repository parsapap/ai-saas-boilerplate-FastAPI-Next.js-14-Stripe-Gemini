import pytest
from httpx import AsyncClient


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
    
    # Verify plan types
    plan_types = [plan["type"] for plan in data]
    assert "free" in plan_types
    assert "pro" in plan_types
    assert "team" in plan_types
