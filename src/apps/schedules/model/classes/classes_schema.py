from src.models import BaseSchema
from datetime import date

class Classes(BaseSchema):
    id: int
    name: str
    number_students: int 