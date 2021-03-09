from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.postgresql_db import get_db
from db.redis import Redis, get_redis_database
from models.user import User, User_create
from models.token import TokenResponse
from authentication.utils import (
    authentication_user,
    create_user,
    send_verfication_email,
    update_user_state,
)
from authentication.security import (
    create_access_token,
    get_password_hash,
    oauth2_scheme,
    validate_email,
    decode_token,
)

auth_router = APIRouter()


@auth_router.post("/signup/")
async def sign_up(
    *,
    user_query: OAuth2PasswordRequestForm = Depends(),
    email: str = Body(...),
    db: Session = Depends(get_db)
):
    if not await validate_email(email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="email is not valid!"
        )
    hashed_password = get_password_hash(user_query.password)
    user_query_dict = {
        "username": user_query.username,
        "password": hashed_password,
        "email": email,
    }
    user_object = User_create(**user_query_dict)
    if create_user(user_object, db):
        access_token = create_access_token(
            data={"user": user_query.username, "email": email}
        )
        url = "http://127.0.0.1:8000/signup/" + access_token
        await send_verfication_email(url, email)
        return {"Response": "Successfully singed up, please confirm your Email."}
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="username is taken!"
        )


@auth_router.get("/signup/{access_token}", response_model=TokenResponse)
async def active_user(
    access_token: str,
    rd: Redis = Depends(get_redis_database),
    db: Session = Depends(get_db),
):
    user = decode_token(access_token)
    if user:
        update_user_state(user.username, True, db)
        access_token_expires = timedelta(minutes=30)
        rd.set(access_token, user.username, access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="your link expired!"
        )


@auth_router.post("/signin/", response_model=TokenResponse)
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    rd: Redis = Depends(get_redis_database),
):
    user = authentication_user(
        conn=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="please confirm your email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"user": user.username}
    )
    rd.set(access_token, user.username, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
