
from src.apps.schedules.model.assignments_courses.assignment_course_model import *
from src.apps.schedules.model.assignments_courses.assignment_course_schema import *
from src.apps.schedules.model.availabilities.availabilities_model import *
from src.apps.schedules.model.availabilities.availabilities_schema import *
from src.apps.schedules.model.classes.classes_model import *
from src.apps.schedules.model.classes.classes_schema import *
from src.apps.schedules.routes.classes.classes_route import \
    router as ClassesRouter
from src.apps.schedules.services.classes.classes_service import *
from src.apps.schedules.model.day_type.day_type_model import *
from src.apps.schedules.model.day_type.day_type_schema import *
from src.apps.schedules.routes.day_type.day_type_route import \
    router as DayTypeRouter
from src.apps.schedules.model.educational_courses.educational_courses_model import *
from src.apps.schedules.model.educational_courses.educational_courses_schema import *
from src.apps.schedules.routes.educational_courses.educational_courses_route import \
    router as EducationalCoursesRouter
from src.apps.schedules.model.subjects.subjects_model import *
from src.apps.schedules.model.subjects.subjects_schema import *
from src.apps.schedules.model.years_groups.years_groups_model import *
from src.apps.schedules.model.years_groups.years_groups_schema import *
from src.apps.schedules.routes.years_groups.years_groups_route import \
    router as YearsGroupsRouter
from src.apps.schedules.model.years_groups_educational_courses.years_groups_educational_courses_model import *
from src.apps.schedules.model.years_groups_educational_courses.years_groups_educational_courses_schema import *
from src.apps.schedules.routes.years_groups_educational_courses.years_groups_educational_courses_route import \
    router as YearsGroupsEducationalCoursesRouter
from src.apps.schedules.model.availabilities.availabilities_model import *
from src.apps.schedules.model.subjects.subjects_model import *
from src.apps.schedules.routes.assignments_courses.assignment_course_route import \
    router as AssignmentCourseRouter
from src.apps.schedules.routes.availabilities.availabilities_route import \
    router as AvailabilitiesRouter
from src.apps.schedules.routes.subjects.subjects_route import \
    router as SubjectsRouter
from src.apps.schedules.services.assignments_courses.assignment_course_service import *
