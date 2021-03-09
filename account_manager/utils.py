from sqlalchemy.orm import Session
from loguru import logger

from db import models


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
