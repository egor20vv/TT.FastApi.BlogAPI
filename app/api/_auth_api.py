from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .dto.auth import TokenDataView, RegisterUserDTO
from utils.cript import (
    create_access_token, 
    create_refrash_token, 
    JWTData, 
    verify_password,
    get_password_hash
)
from db.funcs.user import get_user_by_username, is_user, create_user
from db.entity import UserEntity

auth_route = APIRouter(prefix='/auth', tags=['Auth'])


def generate_tokens(username: str) -> TokenDataView:
    data = JWTData(sub=username)
    return TokenDataView(username=username, 
                         access_token=create_access_token(data),
                         refrash_token=create_refrash_token(data))


@auth_route.post('/login', 
                 summary='Login to accout', 
                 response_model=TokenDataView)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # set exception
    no_user_exception = HTTPException(status.HTTP_401_UNAUTHORIZED,
                                      'User with passed credentials is not found')
    
    # find the user
    user = await get_user_by_username(form_data.username)
    if not user:
        raise no_user_exception
    
    # parse password
    if verify_password(form_data.password, user.password_hash):
        return generate_tokens(form_data.username)
    else:
        raise no_user_exception


@auth_route.post('/signup', 
                 summary='Sing up a new user', 
                 response_model=TokenDataView)
async def register(register_data: RegisterUserDTO):
    # prevent dublicates
    if await is_user(username=register_data.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            'User with passed username is already exists')
    if await is_user(username=register_data.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            'User with passed email is already exists')
    
    # Convert dto to entity
    dumped_dto = register_data.model_dump()
    dumped_dto['password_hash'] = get_password_hash(register_data.password)
    entity = UserEntity.model_validate(dumped_dto)
    
    # Create entity
    username = await create_user(entity)
    
    # return generated jwt tokens
    return generate_tokens(username=username)
