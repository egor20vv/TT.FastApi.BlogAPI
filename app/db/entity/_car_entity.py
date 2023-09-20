from pydantic import BaseModel


class CarEntity(BaseModel):
    name: str
    color: int
    power: float
