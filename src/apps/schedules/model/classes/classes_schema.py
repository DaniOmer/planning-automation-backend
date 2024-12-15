from pydantic import BaseModel
from src.models import BaseSchema

class ClassCreate(BaseSchema):
    name: str
    number_students: int
    years_group_id: int

class ClassResponse(BaseModel):
    id: int
    name: str
    number_students: int
    years_group_id: int