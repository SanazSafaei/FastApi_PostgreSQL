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
from account_manager.utils import (
    get_user_db,
    email_is_available,
    update_user,
    get_admin_permission,
)

modify_accounts_router = APIRouter(prefix="/modify_accounts", tags=["admin pannel"])


@modify_accounts_router.post("/password")
async def modify_password_accounts(
    account_username: str = Form(...),
    account_new_password: str = Form(...),
    admin: User_base = Depends(get_admin_permission),
    db: Session = Depends(get_db),
):
    password_hash = get_password_hash(account_new_password)
    update_user(
        username=account_username,
        conn=db,
        field_to_update="password",
        new_var=password_hash,
    )
    return {"Response": "User's password successfully updated."}


@modify_accounts_router.post("/change-role")
async def modify_role_accounts(
    account_username: str = Form(...),
    account_new_role: str = Form(...),
    user: User_base = Depends(get_admin_permission),
    db: Session = Depends(get_db),
):
    if account_new_role == "admin":
        role = 1
    elif account_new_role == "user":
        role = 2
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="This role doesn't exsits!",
        )
    update_user(
        username=account_username,
        conn=db,
        field_to_update="role",
        new_var=role,
    )
    return {"Response": "User's role successfully updated."}


@modify_accounts_router.post("/change-email")
async def modify_email_accounts(
    account_username: str = Form(...),
    account_new_email: str = Form(...),
    user: User_base = Depends(get_admin_permission),
    db: Session = Depends(get_db),
):
    if not email_is_available(username=account_username, conn=db, email=account_new_email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="There is an account with the new email!",
        )
    update_user(
        username=account_username,
        conn=db,
        field_to_update="email",
        new_var=account_new_email,
    )
    update_user_state(username=account_username, state=False, conn=db)
    return {"Response": "User's email successfully updated. Please confrim the email."}


@modify_accounts_router.post("/confirm-email")
async def modify_confirm_email_accounts(
    account_username: str = Form(...),
    user: User_base = Depends(get_admin_permission),
    db: Session = Depends(get_db),
):
    update_user(
        username=account_username,
        conn=db,
        field_to_update="is_active",
        new_var=True,
    )
    return {"Response": "User's email successfully confirmed."}