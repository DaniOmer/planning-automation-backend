from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.models import BaseSchema

class AvailabilityBase(BaseSchema):
    comment: Optional[str]
    start_at: datetime
    end_at: datetime
    is_recurring: Optional[bool] = False

class AvailabilityCreate(AvailabilityBase):
    users_id: int

class AvailabilityUpdate(AvailabilityBase):
    pass

class AvailabilityResponse(AvailabilityBase):
    users_id: int
