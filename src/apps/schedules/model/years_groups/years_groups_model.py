from sqlalchemy import Column, String, Integer, Date
from src.models import Base

class YearsGroups(Base):
    __tablename__ = 'years_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)