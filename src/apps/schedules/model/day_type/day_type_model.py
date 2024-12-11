from sqlalchemy import Column, String, Integer, Date
from src.models import Base

class DayType(Base):
    __tablename__ = 'day_type'

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)