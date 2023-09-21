from fastapi import FastAPI

from api import (auth_route, me_route)
from db import init_db, DbInitData
from utils.config import Configs 


# init db
init_db(DbInitData(
    uri=Configs.NEO4J.DEFAULT.URI,
    dbname=Configs.NEO4J.DEFAULT.DBNAME,
    username=Configs.NEO4J.DEFAULT.USER,
    password=Configs.NEO4J.DEFAULT.PASS
))

# create app
app = FastAPI()
app.include_router(auth_route)
app.include_router(me_route)



