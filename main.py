from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import aiohttp
import asyncio

from authentication.api import auth_router
from configuration.config_file import ALLOWED_HOSTS
from db.monodb_util import connect_to_mongodb, close_mongo_connection

app = FastAPI()

app.add_middleware(
	    CORSMiddleware,
	    allow_origins=ALLOWED_HOSTS or ["*"],
	    allow_credentials=True,
	    allow_methods=["*"],
	    allow_headers=["*"],
	)

app.include_router(auth_router)
app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongo_connection)	

@app.get("/weather/{city}")
async def weather_provider(city: str):
    address = "https://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession(trust_env=True) as weatherApi_session:
        params = {'q': city, 'appid': '1e2f56bd489cf75c7ad85ab8b2b6eaf4'}
        async with weatherApi_session.get(address, params=params) as  resp:
            result = await resp.json()
            return {"result": result}

