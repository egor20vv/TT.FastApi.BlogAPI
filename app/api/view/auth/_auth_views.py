from pydantic import BaseModel


class TokenDataView(BaseModel):
    username: str
    access_token: str
    refrash_token: str
    
