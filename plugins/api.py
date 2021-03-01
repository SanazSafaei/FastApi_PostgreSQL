from fastapi import APIRouter,Depends
import aiohttp
import asyncio

from authentication.utils import get_current_user
from models.user import User_base

plugins_router = APIRouter()


@plugins_router.get("/weather/{city}")
async def weather_provider(city: str, user: User_base= Depends(get_current_user)):
    address = "https://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession(trust_env=True) as weatherApi_session:
        params = {'q': city, 'appid': '1e2f56bd489cf75c7ad85ab8b2b6eaf4'}
        async with weatherApi_session.get(address, params=params) as  resp:
            result = await resp.json()
            return {"result": result}