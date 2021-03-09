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

modify_accounts_router = APIRouter(prefix="/modify_accounts", tags=["admin pannel"])

@modify_accounts_router.post("/password")
async def modify_password_accounts(
    account_username : str = Form(...),
    account_new_password : str = Form(...),
    user: User_base = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_db = get_user_db(username = user.username , conn = db)
    if user_db.role != 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Sorry, you don't have access!",
        )
    else:
        password_hash = get_password_hash(account_new_password)
        update_user(
            username= account_username,
            conn=db,
            field_to_update="password",
            new_var=password_hash,
        )
        return {"Response": "Password successfully updated."}
    