from pydantic import BaseModel

class DayTypeCreate(BaseModel):
    type: str

class DayTypeResponse(BaseModel):
    id: int
    type: str

    class Config:
        orm_mode = True