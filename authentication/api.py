from fastapi import FastAPI, APIRouter, Form, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from aiofile import AIOFile,async_open,LineReader, Writer
import ast

from models.user import User,User_base
from models.token import TokenResponse
from authentication.utils import authenticate_user
from authentication.security import create_access_token,get_password_hash


auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("/signup/", response_model = TokenResponse)
async def sign_up(*, user_query: OAuth2PasswordRequestForm = Depends(), email: str = Body(...)):
    hashed_password = get_password_hash(user_query.password)
    user_query_dict = {"username" : user_query.username, "Password" : hashed_password, "Email" : email}
    user_query_str = str(user_query_dict)+"\n"
    async with AIOFile("Credentials.txt", 'a+') as doc:
        writer = Writer(doc)
        async for line in LineReader(doc):
            line = line.replace('\n','')
            user_dict = ast.literal_eval(line)
            if user_query.username == user_dict["username"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        await writer(user_query_str)
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user_query.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        


@auth_router.post("/signin/", response_model = TokenResponse)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    