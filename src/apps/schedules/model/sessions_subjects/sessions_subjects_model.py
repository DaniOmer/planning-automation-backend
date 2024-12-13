from sqlalchemy import (TIMESTAMP, Column, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from src.models import Base


class SessionSubject(Base):
    __tablename__ = "sessions_subjects"

    id = Column(Integer, primary_key=True, index=True)
    classrooms_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=True)
    assignments_subjects_id = Column(Integer, ForeignKey("assignments_subjects.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=True)
    status = Column(Enum("Pending", "Confirmed", "Refused", name="status_enum"), nullable=False, default="Pending")
    start_at = Column(TIMESTAMP, nullable=False)
    end_at = Column(TIMESTAMP, nullable=False)

    classroom_info = relationship("Classroom", backref="sessions_subjects")
    assignment_info = relationship("AssignmentSubject", backref="sessions_subjects")
