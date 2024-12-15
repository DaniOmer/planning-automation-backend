from src.models import BaseSchema

from src.apps.schedules.model.educational_courses.educational_courses_schema import EducationalCourseCreate
from src.apps.schedules.model.years_groups.years_groups_schema import YearsGroupCreate

class YearsGroupsEducationalCoursesSchema(BaseSchema):
    years_group_id: int
    educational_course: EducationalCourseCreate
    day_type: str