from fastapi import FastAPI, Form, Body
from starlette.middleware.cors import CORSMiddleware
import aiohttp
import asyncio

from authentication.api import auth_router
from configuration.config_file import ALLOWED_HOSTS


app = FastAPI()

app.add_middleware(
	    CORSMiddleware,
	    allow_origins=ALLOWED_HOSTS or ["*"],
	    allow_credentials=True,
	    allow_methods=["*"],
	    allow_headers=["*"],
	)

app.include_router(auth_router)
	

@app.get("/weather/{city}")
async def weather_provider(city: str):
    address = "https://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession(trust_env=True) as weatherApi_session:
        params = {'q': city, 'appid': '1e2f56bd489cf75c7ad85ab8b2b6eaf4'}
        async with weatherApi_session.get(address, params=params) as  resp:
            result = await resp.json()
            return {"result": result}