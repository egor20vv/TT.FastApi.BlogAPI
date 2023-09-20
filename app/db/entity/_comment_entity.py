from pydantic import BaseModel

class CommentEntity(BaseModel):
    message: str
