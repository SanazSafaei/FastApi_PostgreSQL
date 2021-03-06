from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import aiohttp
import asyncio

from authentication.utils import get_current_user
from models.user import User_base
from db.mongodb import AsyncIOMotorClient, get_database
from plugins.utils import store_log

plugins_router = APIRouter()


@plugins_router.get("/weather/{city}")
async def weather_provider(
    city: str,
    user: User_base = Depends(get_current_user),
    db: AsyncIOMotorClient = Depends(get_database),
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
                await store_log(conn=db, user=user, request=city, response=result)
                return {"result": result}
    except:
        result = credentials_exception
        await store_log(conn=db, user=user, request=city, response=str(result))
        raise result
