from pydantic import BaseModel
from typing import List


class TileSchema(BaseModel):
    position: int

    class Config:
        orm_mode = True


class BoardSchema(BaseModel):
    id: int
    grid: list
    status: str
    grid_size: List[int]
    url: str

    class Config:
        orm_mode = True
