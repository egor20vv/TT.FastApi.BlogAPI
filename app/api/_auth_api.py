from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from api.view.auth import TokenDataView
from utils.cript import create_access_token, create_refrash_token, JWTData


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
    return generate_tokens(form_data.username)


@auth_route.post('/signup', 
                 summary='Sing up a new user', 
                 response_model=TokenDataView)
async def register(user_name: str, password: str, email: str) -> None:
    return generate_tokens(username=user_name)
