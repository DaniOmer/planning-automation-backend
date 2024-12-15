from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class AssignmentSubjectCreate(BaseModel):
    classes_id: int
    subjects_id: int
    users_id: int
    url_online: Optional[str] = Field(default=None)


class ClassInfo(BaseModel):
    id: int
    name: str
    number_students: int


class SubjectInfo(BaseModel):
    id: int
    name: str
    hourly_volume: float
    session_duration: float
    start_at: date
    end_at: date


class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str


class AssignmentSubjectResponse(BaseModel):
    id: int
    classes_id: int
    subjects_id: int
    users_id: int
    url_online: Optional[str]
    class_info: Optional[ClassInfo]
    subject_info: Optional[SubjectInfo]
    user_info: Optional[UserInfo]
