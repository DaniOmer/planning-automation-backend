from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from src.models import Base

class Availabilities(Base):
    __tablename__ = 'availabilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    users_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    slots = Column(JSONB, nullable=False)
    is_recurring = Column(Boolean, default=False)

    user = relationship("User", backref="availabilities")
