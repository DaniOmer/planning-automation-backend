from src.models import BaseSchema
from pydantic import EmailStr
from datetime import datetime

class InvitationBase(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr

class InvitationCreateSchema(InvitationBase):
    pass

class InvitationReadSchema(InvitationBase):
    id: int
    invited_by: int
    expires_at: datetime
    is_disabled: bool
    created_at: datetime
    expires_at: datetime
