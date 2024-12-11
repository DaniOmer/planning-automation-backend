from src.models import BaseSchema
from pydantic import EmailStr
from datetime import datetime

class InvitationBase(BaseSchema):
    email: EmailStr
    invited_by: int
    token: str
    is_disabled: bool = False

class InvitationCreateSchema(InvitationBase):
    pass

class InvitationReadSchema(InvitationBase):
    id: int
    created_at: datetime
    expires_at: datetime
