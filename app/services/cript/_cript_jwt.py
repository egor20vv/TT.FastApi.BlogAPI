from datetime import timedelta, datetime
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError


SECRET_KEY = "eae39e5a4b9c403e8252ab6d0d237aa13ddea786277f7b602f0263c699c26763"
ALGORITHM = "SH256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30 # expire in 30 minutes
DEFAULT_REFRASH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # expire in 7 days


class JWTData(BaseModel):
    sub: str


def _create_token(data: JWTData, expires_delta: timedelta):
    to_encode = data.dict().copy()
    
    expire = datetime.utcnow() + (expires_delta if expires_delta 
       else timedelta(minutes=30))
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: JWTData, 
                        expires_delta: timedelta = timedelta(
                            minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES
                        )) -> str: 
    return _create_token(data, expires_delta)

def create_refrash_token(data: JWTData,
                          expires_delta: timedelta = timedelta(
                              minutes=DEFAULT_REFRASH_TOKEN_EXPIRE_MINUTES
                          )) -> str:
    return _create_token(data, expires_delta)

def encode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return JWTData.parse_obj(payload)
    except (JWTError, ValidationError):
        return None
