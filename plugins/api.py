from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
import aiohttp
import asyncio

from authentication.utils import get_current_user
from models.user import User_base
from db.postgresql_db import get_db
from plugins.utils import store_log

plugins_router = APIRouter()


@plugins_router.get("/weather/{city}")
async def weather_provider(
    city: str,
    user: User_base = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    address = "https://api.openweathermap.org/data/2.5/weather"
    try:
        async with aiohttp.ClientSession(trust_env=True) as weatherApi_session:
            params = {"q": city, "appid": "1e2f56bd489cf75c7ad85ab8b2b6eaf4"}
            async with weatherApi_session.get(address, params=params) as resp:
                result = await resp.json()
                store_log(conn=db, user=user, request=city, response=result)
                return {"result": result}
    except:
        result = credentials_exception
        store_log(conn=db, user=user, request=city, response=str(result))
        raise result
