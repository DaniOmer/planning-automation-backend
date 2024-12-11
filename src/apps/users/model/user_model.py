from sqlalchemy import Column, String, Integer, Enum
from src.models import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(30))
    role = Column(Enum("admin", "teacher", name='role_enum'))
