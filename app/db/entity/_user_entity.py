from uuid import uuid4
from pydantic import BaseModel


class UserEntity(BaseModel):
    guid: uuid4 # primary
    nickname: str # unique index
    fullname: str 
    email: str # unique
    password_hash: str
    