from fastapi import Depends,HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import re 

from models.user import User
from authentication.security import verify_password, verify_token, decode_token
from db.mongodb import AsyncIOMotorClient
from configuration.config_file import DATABASE_NAME


async def validate_email(email : str):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True  
          
    else:  
        return False

async def get_current_user(token = Depends(verify_token)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = decode_token(token)
    if user is None:
        raise credentials_exception
    return user

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


