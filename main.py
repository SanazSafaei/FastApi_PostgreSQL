from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from authentication.api import auth_router
from plugins.api import plugins_router
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
app.include_router(plugins_router)
app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongo_connection)	


