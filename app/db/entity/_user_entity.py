from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, field_validator
from neo4j.time import DateTime


class UserEntity(BaseModel):
    # guid: uuid4 # primary
    username: str # unique index
    email: str # unique index
    password_hash: str
    
    fullname: str | None = None
    born: datetime | None = None
    photo: str | None = None

    @field_validator('born', mode='before')
    def parse_born(dt: DateTime | datetime | None):
        if not dt:
            return None
        if isinstance(dt, datetime):
            return dt
        else:
            return dt.to_native()
    