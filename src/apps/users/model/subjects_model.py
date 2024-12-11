from sqlalchemy import Column, Integer, String, Date
from src.config.database_service import Base

class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    hourly_volume = Column(Integer)
    start_at = Column(Date)
    end_at = Column(Date)
