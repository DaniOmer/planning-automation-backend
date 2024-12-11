from sqlalchemy import Column, String, Integer, Date, ForeignKey
from src.models import Base

class Classes(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    number_students = Column(Integer, nullable=False)
    years_group_id = Column(Integer, ForeignKey('years_groups.id'), nullable=False)