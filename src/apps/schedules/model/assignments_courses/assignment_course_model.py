from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models import Base


class AssignmentCourse(Base):
    __tablename__ = "assignments_courses"

    id = Column(Integer, primary_key=True, index=True)
    classes_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    courses_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    users_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    url_online = Column(String(255))

    class_info = relationship("Classes", backref="assignments_courses")  # Utilise "Classes" au lieu de "Class"
    course_info = relationship("Subjects", backref="assignments_courses")  # Utilise "Subjects" au lieu de "Subject"
    user_info = relationship("User", backref="assignments_courses")
