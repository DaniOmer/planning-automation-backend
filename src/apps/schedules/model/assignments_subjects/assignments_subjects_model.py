from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.models import Base


class AssignmentSubject(Base):
    __tablename__ = "assignments_subjects"

    id = Column(Integer, primary_key=True, index=True)
    classes_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subjects_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    users_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    url_online = Column(String(255))

    class_info = relationship("Classes", backref="assignments_subjects")
    subject_info = relationship("Subjects", backref="assignments_subjects")
    user_info = relationship("User", backref="assignments_subjects")
    
    __table_args__ = (
        UniqueConstraint('classes_id', 'subjects_id', name='uq_classes_subjects'),
    )
