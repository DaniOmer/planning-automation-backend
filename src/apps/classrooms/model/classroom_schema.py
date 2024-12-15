from pydantic import BaseModel

from src.models import BaseSchema

class ClassroomCreate(BaseSchema):
    name: str
    capacity: int

class ClassroomResponse(BaseSchema):
    id: int
    name: str
    capacity: int

