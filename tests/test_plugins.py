import pytest
from httpx import AsyncClient

from main import app
from authentication.utils import get_current_user
from db.mongodb import get_database
from tests.test_utils import fake_active_user, test_db


# client = TestClient(app)


@pytest.mark.asyncio
async def test_weather_provider():
    app.dependency_overrides[get_current_user] = fake_active_user
    app.dependency_overrides[get_database] = test_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("weather/tehran")
    app.dependency_overrides = {}
    assert response.status_code == 200
    