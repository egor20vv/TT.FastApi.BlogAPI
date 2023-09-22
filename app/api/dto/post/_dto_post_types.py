from datetime import datetime
from typing import List
from pydantic import BaseModel


class PublicatePostDTO(BaseModel):
    title: str
    body: str
    preview_img: str | None = None
    
    
class FullPostView(BaseModel):
    id: str
    creator: str
    title: str
    body: str
    preview_img: str | None = None
    
class ShortPostView(BaseModel):
    id: str
    creator: str
    title: str
    preview_img: str | None = None
    
class ShortRecommendedPostListItem(BaseModel):
    id: int
    creator: str
    title: str
    strenght: int
    normalized_strenght: int
    preview_img: str | None = None
    
class ShortRecommendedPostsListView(BaseModel):
    max_strenght: int
    max_normalized_strenght: int
    short_recs: List[ShortRecommendedPostListItem]
    
class ShortPostOrderdListItemView(ShortPostView):
    index: datetime | int
    
    
class PostCommentView(BaseModel):
    id: str
    publicated: datetime
    by: str
    post: str
    message: str
    likes: int