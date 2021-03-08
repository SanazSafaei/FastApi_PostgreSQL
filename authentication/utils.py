from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
import smtplib, ssl
from loguru import logger

from models.user import User_create
from authentication.security import verify_password, verify_token, decode_token
from db import models
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


def update_user_state(username: str, state: bool, conn: Session):
    user_db = (
        conn.query(models.User)
        .filter(models.User.username == username)
        .update({"is_active": True})
    )
    conn.commit()
    logger.info("email confirmed", user_db)


async def get_current_user(token=Depends(verify_token)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = decode_token(token)
    if (user is None) or (user.is_active):
        raise credentials_exception
    return user


def authentication_user(username: str, password: str, conn: Session):
    user_db = conn.query(models.User).filter(models.User.username == username).first()
    if user_db and verify_password(password, user_db.password):
        logger.info("signed in : ", user_db)
        return user_db
    else:
        return False


def create_user(user: User_create, conn: Session):

    user_db = (
        conn.query(models.User).filter(models.User.username == user.username).first()
    )
    if not user_db:
        user_db = models.User(
            username=user.username,
            email=user.email,
            password=user.password,
        )
        conn.add(user_db)
        conn.commit()
        conn.refresh(user_db)
        logger.info("signed up : ", user_db)
        return True
    else:
        return False
