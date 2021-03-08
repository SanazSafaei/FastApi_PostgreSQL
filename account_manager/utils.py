from sqlalchemy.orm import Session
from loguru import logger

from db import models


def get_user_db(username: str, conn: Session):
    user_db = conn.query(models.User).filter(models.User.username == username).first()
    return user_db


def update_user(username: str, conn: Session, field_to_update: str, new_var: str):
    user_db = (
        conn.query(models.User)
        .filter(models.User.username == username)
        .update({field_to_update: new_var})
    )
    conn.commit()
    msg = field_to_update + " updated!"
    logger.info(msg, user_db)
