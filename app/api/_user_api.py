from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, status

from .utils._depends import get_current_user 
from db.entity import UserEntity
from db.funcs.user import subscribe 
from .dto.post._dto_post_types import ShortPostOrderdListItemView

from db.funcs.post import get_user_posts_by_date_ordered, get_user_posts_by_rate_ordered

user_route = APIRouter(prefix='/user', tags=['User'])


@user_route.post('/{id}/follow',
                 summary='Sub/Unsub on user')
async def sub_on_user(id: str, sub: bool = True, 
                      user: UserEntity = Depends(get_current_user)):
    if id == user.username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='Can not subscribe to yourself')
    
    try:
        await subscribe(user.username, id, 'sub' if sub else 'unsub')
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=', '.join(e.args))
    


@user_route.get('/{id}/post', 
              summary='Get my posts', 
              response_model=list[ShortPostOrderdListItemView])
async def get_my_posts(id: str, skip: int = 0, 
                       limit: int | None = None, 
                       order: Literal['date', 'desc_date', 'rate', 'desc_rate'] = 'desc_date'):
    # return RedirectResponse(f'/user/{user.username}/post', )
    posts = []
    if order in ['date', 'desc_date']:
        posts = await get_user_posts_by_date_ordered(
            id, skip, limit, order == 'desc_date'
        )
    else:
        posts = await get_user_posts_by_rate_ordered(
            id, skip, limit, order == 'desc_rate'
        )
    res = []
    for index, uid, creator, post in posts:
        dumped = post.model_dump()
        dumped.update(index=index, id=uid, creator=creator)
        res.append(ShortPostOrderdListItemView.model_validate(dumped))
    return res
        
