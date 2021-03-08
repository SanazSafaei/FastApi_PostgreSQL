from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from authentication.api import auth_router
from account_manager.api import account_router
from plugins.api import plugins_router
from configuration.config_file import ALLOWED_HOSTS
from db.postgresql_db import engine, SessionLocal
from db import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(plugins_router)