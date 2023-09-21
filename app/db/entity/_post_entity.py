from uuid import uuid4
from pydantic import BaseModel

class PostEntity(BaseModel):
    title: str
    body: str
    preview_img: str | None = None
