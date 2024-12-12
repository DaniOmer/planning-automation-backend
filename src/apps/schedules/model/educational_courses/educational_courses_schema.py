from pydantic import BaseModel
from datetime import date
from src.models import BaseSchema

class EducationalCourseCreate(BaseSchema):
    description: str
    day: date
    day_type: str

class EducationalCourseResponse(BaseSchema):
    id: int
    description: str
    day: date
    day_type: str