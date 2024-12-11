from sqlalchemy import Column, Integer, String

from src.models import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)
    capacity = Column(Integer, nullable=False)
