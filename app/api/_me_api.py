from typing import Annotated, List, Literal
from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from .utils._depends import get_current_user 
from .dto.user._dto_user_types import FullUserView, PatchUserDTO, PatchUserCredentialsDTO
from .dto.auth._dto_auth_types import TokenDataView
from .dto.post._dto_post_types import (
    PublicatePostDTO, 
    FullPostView, 
    ShortPostView, 
    ShortRecommendedPostsListView,
    ShortPostOrderdListItemView
)
from .dto.car._dto_car_pytes import CarView, PublicateCarDTO

from db.entity import UserEntity, PostEntity
from db.funcs.user import delete_user, update_user, is_user, get_user_by_username, get_user_by_email
from db.funcs.post import (
    create_post,
    get_user_posts_by_date_ordered,
    get_user_posts_by_rate_ordered
)

from utils.cript import get_password_hash, create_refrash_token, create_access_token, JWTData


me_route = APIRouter(prefix='/me', tags=['User', 'Me'])


@me_route.get('', summary='Get user info', response_model=FullUserView)
async def get_me(user: UserEntity = Depends(get_current_user)):
    # convert from dto to entity
    return FullUserView.model_validate(user.model_dump())
    

@me_route.delete('', summary='Delete user', response_model=FullUserView)
async def delete_me(user: UserEntity = Depends(get_current_user)):
    await delete_user(user.username)
    return FullUserView.model_validate(user)


@me_route.patch('', summary='Patch user data', response_model=FullUserView)
async def patch_me(user: Annotated[UserEntity, Depends(get_current_user)],
                   patch: PatchUserDTO): 
                #    user: UserEntity = Depends(get_current_user)):
    dumped_patch_data = {k: v for k, v in patch.model_dump().items() if v is not None} 
    updated_user_data = await update_user(user.username, dumped_patch_data)
    return FullUserView.model_validate(updated_user_data.model_dump())
    

@me_route.patch('/cred', summary='Patch user credentials data', response_model=TokenDataView)
async def patch_credentials_me(patch: PatchUserCredentialsDTO, 
                               user: UserEntity = Depends(get_current_user)):
    # dumped_patch_data = {k: v for k, v in patch.model_dump() if v is not None}
    update_query = {}
    if patch.email:
        if await is_user(email=patch.email):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'User with email "{patch.email}" is already exists'
            )
        else:
            update_query['email'] = patch.email
    if patch.username:
        if await is_user(username=patch.username):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'User with username "{patch.username}" is already exists0'
            )
        else:
            update_query['username'] = patch.username
    if patch.password:
        update_query['password_hash'] = get_password_hash(patch.password)
    
    await update_user(user.username, update_query)
    
    return TokenDataView(
        username=user.username,
        access_token=create_access_token(JWTData(sub=user.username)),
        refrash_token=create_refrash_token(JWTData(sub=user.username))
    )
        
    
@me_route.get('/post', 
              summary='Get my posts', 
              response_model=list[ShortPostOrderdListItemView])
async def get_my_posts(skip: int = 0, 
                       limit: int | None = None, 
                       order: Literal['date', 'desc_date', 'rate', 'desc_rate'] = 'desc_date',
                       user: UserEntity = Depends(get_current_user)):
    # return RedirectResponse(f'/user/{user.username}/post', )
    posts = []
    if order in ['date', 'desc_date']:
        posts = await get_user_posts_by_date_ordered(
            user.username, skip, limit, order == 'desc_date'
        )
    else:
        posts = await get_user_posts_by_rate_ordered(
            user.username, skip, limit, order == 'desc_rate'
        )
    res = []
    for index, post in posts:
        dumped = post.model_dump()
        dumped.update(index=index)
        res.append(ShortPostOrderdListItemView.model_validate(dumped))
    return res
    

@me_route.post('/post',
                 summary='Create a post', response_model=FullPostView)
async def publicate_post(post_data: PublicatePostDTO,
                         user: UserEntity = Depends(get_current_user)):
    post_entity = PostEntity.model_validate(post_data.model_dump())
    returned_entity = await create_post(user.username, post_entity)
    return FullPostView.model_validate(returned_entity.model_dump())

@me_route.get('/post/followed',
                summary='Get all posts author\'s you follow', 
                response_model=List[ShortPostView])
async def get_posts_followed(skip: int = 0, limit: int = 10):
    pass

@me_route.get('/post/rec',
                summary='Get recommended posts',
                response_model=ShortRecommendedPostsListView)
async def get_recommended_posts(skip: int = 0, limit: int = 10):
    pass

@me_route.get('/post/{post_id}/likers',
                summary='Get usernames who like your post',
                response_class=RedirectResponse)
async def get_post_names_of_likers(skip: int = 0, limit: int = 10):
    pass

@me_route.post('/car', summary='Publicate your new car', response_model=CarView)
async def publicate_car(car_data: PublicateCarDTO):
    pass
    

