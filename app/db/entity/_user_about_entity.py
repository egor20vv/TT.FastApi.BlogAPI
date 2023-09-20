from pydantic import BaseModel
from datetime import datetime


class UserAboutEntity(BaseModel):
    username: str
    fullname: str
    email: str
    born: datetime
    photo: str
