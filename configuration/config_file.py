from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config("configuration/.env")

SECRET_KEY: Secret = config("SECRET_KEY", cast=str)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALLOWED_HOSTS : List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default= "*") 

#mongodb

DATABASE_NAME= config("DATABASE_NAME")
MONGODB_HOST = config("MONGODB_HOST", default= "mongodb://127.0.0.1:27017" )
MONGODB_PORT = config("MONGODB_PORT", default= "27017")

#redis
REDIS_HOST = config("REDIS_HOST", default= "localhost")
REDIS_PORT = config("REDIS_PORT", default= "6379")
REDIS_PASSWORD = config("REDIS_PASSWORD", default= "")

#smtp
SMTP_PORT = config("SMTP_PORT")
SMTP_EMAIL = config("SMTP_EMAIL")
SMTP_PASSWORD = config("SMTP_PASSWORD")
MESSAGE = """\
        Subject: Verfication!

        please click on the link blow.\n"""