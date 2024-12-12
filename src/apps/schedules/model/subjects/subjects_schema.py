from pydantic import BaseModel
from datetime import date
from typing import Optional

class SubjectBase(BaseModel):
    name: str
    hourly_volume: Optional[int]
    session_duration: Optional[float]
    start_at: Optional[date]
    end_at: Optional[date]

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int

    class Config:
        orm_mode = True
