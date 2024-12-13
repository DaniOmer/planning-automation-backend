from sqlalchemy import Column, String, Integer, Date
from src.models import Base

class EducationalCourses(Base):
    __tablename__ = 'educational_courses'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    day = Column(Date, nullable=False)