from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import smtplib, ssl
from loguru import logger

from models.user import User
from authentication.security import verify_password, verify_token, decode_token
from db.mongodb import AsyncIOMotorClient
from configuration.config_file import (
    DATABASE_NAME,
    SMTP_EMAIL,
    SMTP_PASSWORD,
    SMTP_PORT,
    MESSAGE,
)


async def send_verfication_email(url: str, receiver_email: str):
    txt = MESSAGE + url
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", int(SMTP_PORT), context=context) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, receiver_email, txt)
        logger.info("confirm email sent!")


async def update_user_state(username: str, state: bool, conn: AsyncIOMotorClient):
    user_db = await conn[DATABASE_NAME]["user"].update_one(
        {"username": username}, {"$set": {"is_active": state}}
    )
    logger.info("email confirmed", user_db)


async def get_current_user(token=Depends(verify_token)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = decode_token(token)
    if user is None:
        raise credentials_exception
    return user


async def authentication_user(username: str, password: str, conn: AsyncIOMotorClient):
    user_db = await conn[DATABASE_NAME]["user"].find_one({"username": username})
    logger.info("signed in : ", user_db)
    if user_db and verify_password(password, user_db["password"]):
        return user_db
    else:
        return False


async def create_user(user: User, conn: AsyncIOMotorClient):
    user_db = await conn[DATABASE_NAME]["user"].find_one({"username": user.username})
    logger.info("signed up : ", user_db)
    if not user_db:
        row = await conn[DATABASE_NAME]["user"].insert_one(user.dict())
        return True
    else:
        return False
