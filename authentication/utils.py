from models.user import User
from authentication.security import verify_password
from db.mongodb import AsyncIOMotorClient
from configuration.config_file import DATABASE_NAME


async def authentication_user(username: str, password: str, conn : AsyncIOMotorClient): 
    user_db = await conn[DATABASE_NAME]['user'].find_one({"username": username})
    if user_db and verify_password(password, user_db['password']):
        return user_db
    else:
        return False 


async def create_user(user : User, conn : AsyncIOMotorClient):
    user_db = await conn[DATABASE_NAME]['user'].find_one({"username": user.username})
    if not user_db:
        row = await conn[DATABASE_NAME]['user'].insert_one(user.dict())
        return True
    else:
        return False


