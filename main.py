from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
from aiofile import AIOFile,async_open,LineReader, Writer
import ast
import aiohttp
import asyncio, urllib


class User_base(BaseModel):
    UserName: str
    Password: str

class User(User_base):
    Email: str


app = FastAPI()

@app.post("/signup/")
async def sign_up(user: User= Body(...)):
    user_str = str(user.dict())+"\n"
    user_all=[]
    async with AIOFile("Document.txt", 'a+') as doc:
        writer = Writer(doc)
        async for line in LineReader(doc):
            data = line.replace('\n','')
            old_user = ast.literal_eval(data)
            if user.UserName == old_user["UserName"]:
                return {"result" : "User exists!"}
        await writer(user_str)
        doc.close()
        return {"result" : "Congrats you singed up!"}


@app.post("/signin/")
async def sign_in(*, user: str = Form(...), password: str=Form(...), city: str):
    session = False
    async with AIOFile("Document.txt", 'r') as doc:
        async for line in LineReader(doc):
            data = line.replace('\n','')
            old_user = ast.literal_eval(data)
            if user == old_user["UserName"]:
                if password == old_user ["Password"]:
                    session= True
                else:
                     return {"result" : "Password is wrong."}
        doc.close()
    if session :
        address = "https://api.openweathermap.org/data/2.5/weather?q="+ city+ "&appid=1e2f56bd489cf75c7ad85ab8b2b6eaf4"
        async with aiohttp.ClientSession(trust_env=True) as session:
            params = {'q': city, 'appid': '1e2f56bd489cf75c7ad85ab8b2b6eaf4'}
            async with session.get(address) as  resp:
                result = await resp.json()
                return {"result": result}
    else:
        return {"result" : "Please sing up first."}


