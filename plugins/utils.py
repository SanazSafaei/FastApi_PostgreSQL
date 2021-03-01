from db.mongodb import AsyncIOMotorClient, get_database
from models.user import User_base
from configuration.config_file import DATABASE_NAME

async def store_log(conn : AsyncIOMotorClient, user : User_base, request, response):
    dpocument={
        'user' : user,
        'request' : request,
        'response' : response
    }
    result = await conn[DATABASE_NAME]['log'].insert({"username": username})