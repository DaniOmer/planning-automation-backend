from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models import Base

class YearsGroupsEducationalCourses(Base):
    __tablename__ = 'years_groups_educational_courses'

    years_group_id: Mapped[int] = mapped_column(ForeignKey('years_groups.id'), primary_key=True)
    educational_courses_id: Mapped[int] = mapped_column(ForeignKey('educational_courses.id'), primary_key=True)
    day_type_id: Mapped[int] = mapped_column(ForeignKey('day_type.id'), nullable=False)

    years_group = relationship("YearsGroup", backref="years_groups_educational_courses")
    educational_course = relationship("EducationalCourse", backref="years_groups_educational_courses")
    day_type = relationship("DayType", backref="years_groups_educational_courses")