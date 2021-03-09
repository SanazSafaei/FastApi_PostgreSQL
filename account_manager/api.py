from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy.orm import Session
from loguru import logger

from authentication.utils import get_current_user
from db.postgresql_db import get_db
from models.user import User_create, User_base
from authentication.security import verify_password, get_password_hash
from authentication.utils import update_user_state
from account_manager.utils import get_user_db, email_is_available, update_user

account_router = APIRouter(tags=["modify account"])


@account_router.post("/edit-profile/password")
async def update_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    user: User_base = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if new_password == old_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="new password can't be the same as old password!",
        )
    user_db = get_user_db(user.username, db)
    logger.error(user_db.password)
    if verify_password(old_password, user_db.password):
        password_hash = get_password_hash(new_password)
        update_user(
            username=user.username,
            conn=db,
            field_to_update="password",
            new_var=password_hash,
        )
        return {"Response": "Password successfully updated."}
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="old password is not correct!"
        )


@account_router.post("/edit-profile/email")
async def update_email(
    old_email: str = Form(...),
    new_email: str = Form(...),
    user: User_base = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if new_email == old_email:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="new email can't be the same as old email!",
        )
    user_db = get_user_db(user.username, db)
    if not email_is_available(username=user_db.username, conn=db, email=new_email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="There is an account with your new email!",
        )
    if user_db.email == old_email:
        update_user(
            username=user.username, conn=db, field_to_update="email", new_var=new_email
        )
        update_user_state(username=user.username, state=False, conn=db)
        return {"Response": "Email successfully updated, please confirm your Email."}
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="old email is not correct!"
        )


@account_router.post("/modify-accounts/")
async def modify_accounts():
    pass