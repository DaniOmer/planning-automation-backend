from typing import Optional

from pydantic import BaseModel, Field


class AssignmentCourseCreate(BaseModel):
    classes_id: int
    courses_id: int
    users_id: int
    url_online: Optional[str] = Field(default=None)


class ClassInfo(BaseModel):
    id: int
    name: str

class CourseInfo(BaseModel):
    id: int
    name: str

class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str

class AssignmentCourseResponse(BaseModel):
    id: int
    classes_id: int
    courses_id: int
    users_id: int
    url_online: Optional[str]
    class_info: Optional[ClassInfo]
    course_info: Optional[CourseInfo]
    user_info: Optional[UserInfo]


