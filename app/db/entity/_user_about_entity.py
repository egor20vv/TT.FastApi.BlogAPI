# from pydantic import BaseModel, field_validator
# from datetime import datetime
# from neo4j.time import DateTime


# class UserAboutEntity(BaseModel):
#     username: str
#     fullname: str
#     email: str
#     born: datetime
#     photo: str

#     @field_validator('born', mode='before')
#     def parse_born(dt: DateTime | datetime):
#         if isinstance(dt, datetime):
#             return dt
#         else:
#             return dt.to_native()
