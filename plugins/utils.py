from db.mongodb import AsyncIOMotorClient, get_database
from models.user import User_base
from configuration.config_file import DATABASE_NAME
from loguru import logger

async def store_log(conn : AsyncIOMotorClient, user : User_base, request, response):
    document={
        'user' : user.dict(),
        'request' : request,
        'response' : response
    }
    result = await conn[DATABASE_NAME]['log'].insert_one({"document": document})
    logger.info("restored to database : ", document)