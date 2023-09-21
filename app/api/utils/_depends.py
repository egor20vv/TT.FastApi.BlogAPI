from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pytz import UTC

from utils.cript import encode_token
from db.entity import UserEntity
from db.funcs.user import get_user_by_username, is_user


_reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

def _generate_auth_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )


async def get_current_user(token: str = Depends(_reuseable_oauth)) -> UserEntity:
    token_data = encode_token(token)
    
    if not token_data:
        raise _generate_auth_exception('Could not validate credetials')
    
    if token_data.exp.replace(tzinfo=UTC) < datetime.now(UTC):
        raise _generate_auth_exception('Token exired')
    
    if not await is_user(username=token_data.sub):
        raise _generate_auth_exception('User not found')
    
    return await get_user_by_username(token_data.sub)
    