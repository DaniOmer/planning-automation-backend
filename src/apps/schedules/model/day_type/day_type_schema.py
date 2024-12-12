from src.models import BaseSchema

class DayTypeCreate(BaseSchema):
    type: str

class DayTypeResponse(BaseSchema):
    id: int
    type: str