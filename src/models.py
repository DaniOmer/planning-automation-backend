from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass 

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True