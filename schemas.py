from pydantic import BaseModel


class TileSchema(BaseModel):
    position: int

    class Config:
        orm_mode = True
