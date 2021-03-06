import pytest
from httpx import AsyncClient

from tests.test_utils import fake_active_user, test_db, fake_new_user
from authentication.utils import authentication_user, create_user


@pytest.mark.asyncio
async def test_authenticate_user():
    user = fake_active_user()
    db = await test_db()
    respones = await authentication_user(user.username, "12345", db)
    assert user.username == respones["username"]


@pytest.mark.asyncio
async def test_create_user():
    user = fake_new_user()
    db = await test_db()
    response = await create_user(user, db)
    assert response
