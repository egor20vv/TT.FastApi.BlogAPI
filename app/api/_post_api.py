from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from .utils._depends import get_current_user 
from db.entity import UserEntity, PostEntity
from db.funcs.post import like_post, get_post_likers, get_post_comments, create_comment

from .dto.user._dto_user_types import ShortUserView
from .dto.post._dto_post_types import PostCommentView

post_route = APIRouter(prefix='/post', tags=['Post'])


@post_route.post('{id}/like',
                 summary='Like post')
async def post_send_like(id: str, like: bool = True,
                         user: UserEntity = Depends(get_current_user)):
    try:
        await like_post(user.username, id, 'like' if like else 'unlike')
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=', '.join(e.args)) 
        
@post_route.get('{id}/liked',
                summary='Get users likes a post',
                response_model=List[ShortUserView])
async def get_likers_of_post(id: str):
    try:
        models = await get_post_likers(id)
        return [ShortUserView.model_validate(u.model_dump()) 
                for u in await get_post_likers(id)] 
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='No one found')

@post_route.get('/{post_id}/comments',
                summary='Get all post comments',
                response_model=list[PostCommentView])
async def get_comments(post_id: str, skip: int = 0, limit: int | None = None):
    try:
        raw_comments = await get_post_comments(post_id, skip, limit)
        return [PostCommentView(**comment) for comment in raw_comments]
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='No comments')

@post_route.post('/{post_id}/comments',
                 summary='Post a comment to the post',
                 response_model=PostCommentView)
async def post_comment(post_id: str, message: str,
                       user: UserEntity = Depends(get_current_user)):
    try:
        raw_comment = await create_comment(user.username, post_id, message)
        return PostCommentView(**raw_comment)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=', '.join(e.args))

@post_route.post('/{post_id}/comments/{comment_id}',
                 summary='like a comment')
async def like_comment(post_id: str, comment_id: str, like: bool = True):
    pass
