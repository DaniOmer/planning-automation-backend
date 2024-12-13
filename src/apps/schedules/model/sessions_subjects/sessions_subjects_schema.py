from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ClassroomInfo(BaseModel):
    id: int
    name: str
    capacity: int


class ClassInfo(BaseModel):
    id: int
    name: str
    number_students: int

class SubjectInfo(BaseModel):
    id: int
    name: str
    hourly_volume: float
    session_duration: float
    start_at: datetime
    end_at: datetime

   


class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    
class AssignmentSubjectInfo(BaseModel):
    id: int
    classes_id: int
    subjects_id: int
    users_id: int
    url_online: Optional[str]
    class_info: Optional[ClassInfo]
    subject_info: Optional[SubjectInfo]
    user_info: Optional[UserInfo]

   
class SessionSubjectCreate(BaseModel):
    classrooms_id: Optional[int] = Field(default=None, description="ID of the classroom (nullable)")
    assignments_subjects_id: int = Field(..., description="ID of the assigned subject")
    comment: Optional[str] = Field(default=None, description="Optional comment for the session")
    status: str = Field(..., description="Status of the session")
    start_at: datetime = Field(..., description="Start date and time of the session")
    end_at: datetime = Field(..., description="End date and time of the session")


class SessionSubjectUpdate(BaseModel):
    classrooms_id: Optional[int] = Field(default=None, description="ID of the classroom (nullable)")
    assignments_subjects_id: Optional[int] = Field(default=None, description="ID of the assigned subject")
    comment: Optional[str] = Field(default=None, description="Optional comment for the session")
    status: Optional[str] = Field(default=None, description="Status of the session")
    start_at: Optional[datetime] = Field(default=None, description="Start date and time of the session")
    end_at: Optional[datetime] = Field(default=None, description="End date and time of the session")


class SessionSubjectResponse(BaseModel):
    id: int
    classrooms_id: Optional[int]
    assignments_subjects_id: int
    comment: Optional[str]
    status: str
    start_at: datetime
    end_at: datetime
    classroom_info: Optional[ClassroomInfo]
    assignment_info: Optional[AssignmentSubjectInfo]



   
