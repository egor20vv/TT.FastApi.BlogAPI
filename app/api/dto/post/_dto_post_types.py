from datetime import datetime
from typing import List
from pydantic import BaseModel


class PublicatePostDTO(BaseModel):
    title: str
    body: str
    preview_img: str | None = None
    
    
class FullPostView(BaseModel):
    title: str
    body: str
    preview_img: str | None = None
    
class ShortPostView(BaseModel):
    title: str
    preview_img: str | None = None
    
class ShortRecommendedPostListItem(BaseModel):
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