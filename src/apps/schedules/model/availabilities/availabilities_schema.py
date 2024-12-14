from datetime import datetime
from typing import List
from src.models import BaseSchema


class Slot(BaseSchema):
    start_at: datetime
    end_at: datetime

class AvailabilityBase(BaseSchema):
    slots: List[Slot]

class AvailabilityCreateSchema(AvailabilityBase):
    pass

class AvailabilityUpdateSchema(AvailabilityBase):
    pass

class AvailabilityResponseSchema(AvailabilityBase):
    users_id: int
