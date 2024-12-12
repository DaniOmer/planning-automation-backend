from pydantic import BaseModel
from typing import Optional

class ClassCreate(BaseModel):
    name: str
    number_students: int
    years_group_id: int

class ClassResponse(BaseModel):
    id: int
    name: str
    number_students: int
    years_group_id: int

    class Config:
        orm_mode = True