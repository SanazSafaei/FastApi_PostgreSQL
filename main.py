from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
from aiofile import AIOFile,async_open,LineReader, Writer
import ast
import aiohttp
import asyncio


class User_base(BaseModel):
    UserName: str
    Password: str

class User(User_base):
    Email: str


app = FastAPI()

@app.post("/signup/")
async def sign_up(user_query: User= Body(...)):
    user_query_str = str(user_query.dict())+"\n"
    async with AIOFile("Credentials.txt", 'a+') as doc:
        writer = Writer(doc)
        async for line in LineReader(doc):
            line = line.replace('\n','')
            user_dict = ast.literal_eval(line)
            if user_query.UserName == user_dict["UserName"]:
                return {"result" : "User exists!"}
        await writer(user_query_str)
        return {"result" : "Congrats you singed up!"}


@app.post("/signin/")
async def sign_in(*, username: str = Form(...), password: str=Form(...)):
    async with AIOFile("Credentials.txt", 'r') as doc:
        async for line in LineReader(doc):
            line = line.replace('\n','')
            user_dict = ast.literal_eval(line)
            print(username, password , user_dict["UserName"], user_dict ["Password"])
            if username == user_dict["UserName"] and password==user_dict ["Password"]:
                return {"result" : "You are loged in"}
        else:
            return {"result" : "Username or Password is wrong."}   


@app.get("/weather/{city}")
async def weather_provider(city: str):
    address = "https://api.openweathermap.org/data/2.5/weather"
    async with aiohttp.ClientSession(trust_env=True) as weatherApi_session:
        params = {'q': city, 'appid': '1e2f56bd489cf75c7ad85ab8b2b6eaf4'}
        async with weatherApi_session.get(address, params=params) as  resp:
            result = await resp.json()
            return {"result": result}