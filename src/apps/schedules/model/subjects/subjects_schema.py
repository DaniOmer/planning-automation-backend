from datetime import date
from typing import Optional
from src.models import BaseSchema

class SubjectBase(BaseSchema):
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
