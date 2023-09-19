from fastapi import FastAPI

from api import (auth_route)

# create app
app = FastAPI()
app.include_router(auth_route)



