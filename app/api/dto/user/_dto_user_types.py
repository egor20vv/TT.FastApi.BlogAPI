from datetime import datetime
from pydantic import BaseModel


class FullUserView(BaseModel):
    username: str
    email: str
    
    fullname: str | None = None
    born: datetime | None = None
    photo: str | None = None
    

class PatchUserDTO(BaseModel):
    fullname: str | None = None
    born: datetime | None = None
    photo: str | None = None
    

class PatchUserCredentialsDTO(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    