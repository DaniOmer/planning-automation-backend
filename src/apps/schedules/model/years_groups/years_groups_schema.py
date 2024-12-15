from pydantic import BaseModel
from src.models import BaseSchema

class YearsGroupCreate(BaseSchema):
    name: str

class YearsGroupResponse(BaseSchema):
    id: int
    name: str