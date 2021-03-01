from fastapi import APIRouter, Body, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from db.mongodb import AsyncIOMotorClient, get_database
from models.user import User
from models.token import TokenResponse
from authentication.utils import authentication_user,create_user
from authentication.security import create_access_token,get_password_hash,oauth2_scheme
from db.redis import Redis, get_redis_database

auth_router = APIRouter()


@auth_router.post("/signup/", response_model = TokenResponse)
async def sign_up(*, user_query: OAuth2PasswordRequestForm = Depends(), email: str = Body(...),
                 db: AsyncIOMotorClient = Depends(get_database), rd: Redis = Depends(get_redis_database)):
    hashed_password = get_password_hash(user_query.password)
    user_query_dict = {"username" : user_query.username, "password" : hashed_password, "email" : email}
    user_object = User(**user_query_dict)
    if await create_user(user_object, db):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={"user": user_query.username, "email": email})
        rd.set(access_token,user_query.username, access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
	            status_code=HTTP_400_BAD_REQUEST, detail="username is taken!"
	        )
        

@auth_router.post("/signin/", response_model = TokenResponse)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db : AsyncIOMotorClient = Depends(get_database), rd: Redis = Depends(get_redis_database)):
    user = await authentication_user(conn=db,username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"user": user['username'],"email": user['email']})
    rd.set(access_token, user["username"], access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
    