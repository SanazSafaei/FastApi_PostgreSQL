from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from loguru import logger

from authentication.security import verify_token, decode_token
from db import models

async def get_admin_permission(token=Depends(verify_token)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, sorry you don't have access",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = decode_token(token)
    if (user is None) or not (user.is_active) or user.role != 1:
        logger.error(user)
        raise credentials_exception
    return user

def get_user_db(username: str, conn: Session):
    user_db = conn.query(models.User).filter(models.User.username == username).first()
    return user_db


def get_user_db_by_email(email: str, conn: Session):
    user_db = conn.query(models.User).filter(models.User.email == email).first()
    return user_db


def email_is_available(username: str, conn: Session, email: str):
    email_user = get_user_db_by_email(email, conn)
    if email_user and email_user.username != username:
        return False
    else:
        return True


def update_user(username: str, conn: Session, field_to_update: str, new_var: str):
    user_db = (
        conn.query(models.User)
        .filter(models.User.username == username)
        .update({field_to_update: new_var})
    )
    conn.commit()
    msg = field_to_update + " updated!"
    logger.info(msg, user_db)
