from sqlalchemy import ForeignKey, Integer, Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models import Base

class YearsGroupsEducationalCourses(Base):
    __tablename__ = 'years_groups_educational_courses'

    day_type = Column(String(255), nullable=False)
    years_group_id: Mapped[int] = mapped_column(ForeignKey('years_groups.id'), primary_key=True)
    educational_courses_id: Mapped[int] = mapped_column(ForeignKey('educational_courses.id'), primary_key=True)

    years_group = relationship("YearsGroups", backref="years_groups_educational_courses")
    educational_course = relationship("EducationalCourses", backref="years_groups_educational_courses")