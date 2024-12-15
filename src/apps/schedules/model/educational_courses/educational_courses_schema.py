from datetime import date
from src.models import BaseSchema

class EducationalCourseCreate(BaseSchema):
    day: date

class EducationalCourseResponse(BaseSchema):
    id: int
    day: date