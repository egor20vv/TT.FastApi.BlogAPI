from uuid import uuid4
from pydantic import BaseModel

class PostEntity(BaseModel):
    guid: uuid4
    title: str
    body: str
    preview_img: str
