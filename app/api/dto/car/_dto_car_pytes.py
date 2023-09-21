from pydantic import BaseModel


class PublicateCarDTO(BaseModel):
    model: str
    name: str
    color: int
    power: float


class CarView(BaseModel):
    model: str
    name: str
    color: int
    power: float
    