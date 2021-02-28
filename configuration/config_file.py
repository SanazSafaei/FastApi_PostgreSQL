from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config("configuration/.env")

SECRET_KEY: Secret = config("SECRET_KEY", cast=str)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALLOWED_HOSTS : List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)

#############################################
DATABASE_NAME= config("DATABASE_NAME")
MONGODB_HOST = config("MONGODB_HOST")
MONGODB_PORT = config("MONGODB_PORT")
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_PASSWORD = config("REDIS_PASSWORD")