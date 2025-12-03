import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker

fake = Faker()


@pytest.fixture
async def client():
    """Create test client without database"""
    from app.main import app
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data():
    """Generate test user data"""
    return {
        "email": fake.email(),
        "password": "TestPass123!",
        "full_name": fake.name()
    }


@pytest.fixture
def test_org_data():
    """Generate test organization data"""
    slug = fake.slug()
    return {
        "name": fake.company(),
        "slug": slug,
        "description": fake.text(max_nb_chars=200)
    }
