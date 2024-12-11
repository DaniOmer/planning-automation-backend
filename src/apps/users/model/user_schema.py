from src.models import BaseSchema
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "teacher"

class UserCreate(BaseSchema):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    role: RoleEnum

class UserLogin(BaseSchema):
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