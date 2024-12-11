from pydantic import BaseModel

class YearsGroupCreate(BaseModel):
    name: str

class YearsGroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True