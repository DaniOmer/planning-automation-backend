from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models import Base

class Invitation(Base):
    __tablename__ = 'invitation'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    invited_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    is_disabled = Column(Boolean, default=False)

    inviter = relationship("User", backref="invitations_sent")
