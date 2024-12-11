from src.models import BaseSchema
from datetime import date

class EducationalCourses(BaseSchema):
    id: int
    description: str
    day: date