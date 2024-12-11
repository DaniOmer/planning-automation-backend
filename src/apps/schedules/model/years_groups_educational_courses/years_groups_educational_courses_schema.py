from src.models import BaseSchema

class YearsGroupsEducationalCoursesSchema(BaseSchema):
    years_group_id: int
    educational_courses_id: int
    day_type_id: int