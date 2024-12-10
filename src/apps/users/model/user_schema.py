from src.models import BaseSchema
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class UserCreate(BaseSchema):
    first_name: str
    last_name: str
    email: str
    password: str
    role: RoleEnum

class UserResponse(BaseSchema):
    id: int
    first_name: str
    last_name: str
    password: str
    email: str
    role: RoleEnum
