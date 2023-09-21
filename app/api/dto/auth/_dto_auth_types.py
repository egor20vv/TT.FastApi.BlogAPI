from datetime import datetime
from pydantic import BaseModel


class TokenDataView(BaseModel):
    username: str
    access_token: str
    refrash_token: str


class RegisterUserDTO(BaseModel):
    username: str
    email: str
    password: str
    
    fullname: str | None = None
    born: datetime | None = None
    photo: str | None = None
