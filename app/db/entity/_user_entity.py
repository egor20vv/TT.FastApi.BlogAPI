from pydantic import BaseModel
# from enum import Enum


# class UserRoles(Enum):
#     Simple = 0
#     Admin = 1


class UserEntity(BaseModel):
    guid: int # primary
    nickname: str # unique index
    fullname: str 
    email: str # unique
    password_hash: str
    