from enum import Enum
from typing import Optional, List
from pydantic import EmailStr

from src.models import BaseSchema

class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"

class UserBase(BaseSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone_number: Optional[str]

class UserCreateSchema(UserBase):
    password: str

class UserCreateByInvitationSchema(BaseSchema):
    user: UserCreateSchema
    token: str

class UserLoginSchema(BaseSchema):
    email: str
    password: str

class UserResponse(BaseSchema):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: RoleEnum

class LoginResponse(BaseSchema):
    user: UserResponse
    access_token: str

class UserRead(UserBase):
    id: int
    created_by: Optional[int]

class UserWithCreatedUsers(UserRead):
    created_users: List["UserRead"]



