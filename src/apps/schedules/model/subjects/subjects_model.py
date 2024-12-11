from sqlalchemy import Column, Integer, String, Date, Float
from src.models import Base

class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    hourly_volume = Column(Integer)
    session_duration = Column(Float)
    start_at = Column(Date)
    end_at = Column(Date)
