from motor.motor_asyncio import AsyncIOMotorClient

from configuration.config_file import MONGODB_HOST, MONGODB_PORT
from db.mongodb import db


async def connect_to_mongodb() -> None:
    db.client = AsyncIOMotorClient(MONGODB_HOST, int(MONGODB_PORT))


async def close_mongo_connection():
    db.client.close()