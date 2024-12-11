from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from src.models import Base

class Availabilities(Base):
    __tablename__ = 'availabilities'

    users_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    comment = Column(String(1000))
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, default=False)
