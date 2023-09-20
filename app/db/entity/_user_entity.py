from uuid import uuid4
from pydantic import BaseModel


class UserEntity(BaseModel):
    guid: uuid4 # primary
    username: str # unique index
    email: str # unique index
    password_hash: str
    