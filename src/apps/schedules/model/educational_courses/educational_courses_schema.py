from pydantic import BaseModel
from datetime import date

class EducationalCourseCreate(BaseModel):
    description: str
    day: date

class EducationalCourseResponse(BaseModel):
    id: int
    description: str
    day: date

    class Config:
        orm_mode = True