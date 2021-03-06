import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import User_base, User
from configuration.config_file import MONGODB_HOST, MONGODB_PORT

count = 0


class DataBase:
    client: AsyncIOMotorClient = None


def fake_active_user():
    user_dict = {"username": "test", "email": "ssanazz@yahoo.com", "is_active": True}
    return User_base(**user_dict)


def fake_new_user():
    global count
    user_dict = {
        "username": "this_is_test" + str(count),
        "email": "ssanazz@yahoo.com",
        "password": "12345",
    }
    count += 1
    return User(**user_dict)


@pytest.mark.asyncio
async def test_db():
    db = DataBase()
    db.client = AsyncIOMotorClient(MONGODB_HOST, int(MONGODB_PORT))
    return db.client
