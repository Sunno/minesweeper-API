from pydantic import BaseModel, validator


class TileSchema(BaseModel):
    position: int

    class Config:
        orm_mode = True


class BoardSchemaResponse(BaseModel):
    id: int
    grid: list
    status: str
    grid_size: int
    mines_number: int
    url: str

    class Config:
        orm_mode = True


class BoardSchema(BaseModel):
    grid_size: int
    mines_number: int

    @validator('mines_number')
    def mines_number_validation(cls, v, values, **kwargs):
        if v >= (values['grid_size'] * values['grid_size']):
            raise ValueError('mines_number should be smaller than grid_size^2')
        return v

    @validator('grid_size')
    def greater_than_1(cls, v):
        if v <= 1:
            raise ValueError('grid_size must be greater than 1')
        return v

    class Config:
        orm_mode = True
