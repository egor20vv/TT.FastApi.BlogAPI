from datetime import datetime
from email.policy import HTTP
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from utils.cript import encode_token
from db.entity import UserEntity

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
    tokenData = encode_token(token)
    
    if not tokenData:
        raise _generate_auth_exception('Could not validate credetials')
    
    if tokenData.exp < datetime.utcnow():
        raise _generate_auth_exception('Token exired')
    
    return UserEntity(guid=0, 
                      nickname=tokenData.sub, 
                      fullame=tokenData.sub, 
                      email='aa', 
                      password_hash='1')
    