from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import bcrypt
from passlib.context import CryptContext
from datetime import timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import re

from models.user import User_base
from configuration.config_file import SECRET_KEY, ALGORITHM
from db.redis import Redis, get_redis_database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


async def validate_email(email: str):
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if re.search(regex, email):
        return True

    else:
        return False


def verify_token(
    rd: Redis = Depends(get_redis_database), token: str = Depends(oauth2_scheme)
):
    if rd.get(token):
        return token
    else:
        return False


def decode_token(token=str) -> User_base:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_dict = {"username": payload.get("user"), "email": payload.get("email")}
        user = User_base(**user_dict)
    except JWTError:
        raise credentials_exception
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
