from src.models import BaseSchema
from datetime import date

class DayType(BaseSchema):
    id: int
    type: str