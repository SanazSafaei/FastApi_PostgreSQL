from models.user import User_base
from configuration.config_file import DATABASE_NAME
from sqlalchemy.orm import Session
from loguru import logger

from db import models


def store_log(conn: Session, user: User_base, request, response):
    document = {"user": user.dict(), "request": request, "response": response}
    user_db = (
        conn.query(models.User).filter(models.User.username == user.username).first()
    )
    log_db = models.Log(request=request, response=response, owner_id=user_db.id)
    conn.add(log_db)
    conn.commit()
    conn.refresh(log_db)
    logger.info("restored to database : ", document)