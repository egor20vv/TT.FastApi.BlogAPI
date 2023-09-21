from typing import Annotated, List
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
    ShortRecommendedPostsListView
)
from .dto.car._dto_car_pytes import CarView, PublicateCarDTO

from db.entity import UserEntity
from db.funcs.user import delete_user, update_user


user_route = APIRouter(prefix='/me', tags=['Me'])


@user_route.get('', summary='Get user info', response_model=FullUserView)
async def get_me(user: UserEntity = Depends(get_current_user)):
    # convert from dto to entity
    dumped_user_data = user.model_dump()
    return FullUserView.model_validate(dumped_user_data)
    

@user_route.delete('', summary='Delete user')
async def delete_me(user: UserEntity = Depends(get_current_user)):
    await delete_user(user.username)


@user_route.patch('', summary='Patch user data', response_model=FullUserView)
async def patch_me(user: Annotated[UserEntity, Depends(get_current_user)],
                   patch: PatchUserDTO): 
                #    user: UserEntity = Depends(get_current_user)):
    dumped_patch_data = {k: v for k, v in patch.model_dump() if v is not None} 
    updated_user_data = await update_user(user.username, dumped_patch_data)
    return FullUserView.model_validate(updated_user_data)
    

@user_route.patch('', summary='Patch user credentials data', response_model=TokenDataView)
async def patch_credentials_me(patch: PatchUserCredentialsDTO):
    pass

@user_route.get('/post', 
                summary='Redirects to user/{id}/post', response_class=RedirectResponse)
async def get_my_posts():
    pass

@user_route.post('/post',
                 summary='Create a post', response_model=FullPostView)
async def publicate_post(post_data: PublicatePostDTO):
    pass

@user_route.get('/post/followed',
                summary='Get all posts author\'s you follow', 
                response_model=List[ShortPostView])
async def get_posts_followed(skip: int = 0, limit: int = 10):
    pass

@user_route.get('/post/rec',
                summary='get recommended posts',
                response_model=ShortRecommendedPostsListView)
async def get_recommended_posts(skip: int = 0, limit: int = 10):
    pass

@user_route.get('/post/{post_id}/likers',
                summary='Redirects to /user/{id}/post/{id}/likers',
                response_class=RedirectResponse)
async def get_post_names_of_likers(skip: int = 0, limit: int = 10):
    pass

@user_route.post('/car', summary='Publicate your new car', response_model=CarView)
async def publicate_car(car_data: PublicateCarDTO):
    pass
    

