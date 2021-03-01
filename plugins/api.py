from fastapi import APIRouter
import aiohttp
import asyncio


plugins_router = APIRouter()


@plugins_router.get("/weather/{city}")
async def weather_provider(city: str):
    address = "https://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession(trust_env=True) as weatherApi_session:
        params = {'q': city, 'appid': '1e2f56bd489cf75c7ad85ab8b2b6eaf4'}
        async with weatherApi_session.get(address, params=params) as  resp:
            result = await resp.json()
            return {"result": result}