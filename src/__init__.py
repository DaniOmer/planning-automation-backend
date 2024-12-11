from fastapi import FastAPI

from src.apps.classrooms import ClassroomRouter
from src.apps.users import UserRouter
from src.apps.schedules import ClassesRouter, DayTypeRouter, EducationalCoursesRouter, YearsGroupsRouter, YearsGroupsEducationalCoursesRouter

app = FastAPI(
    title="Planify API with documentation",
    description="This is Planify API.",
    version="1.0.0",
    contact={
        "name": "Planify Team",
        "url": "https://planify.com",
        "email": "planify@infos.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Routers
app.include_router(UserRouter)
app.include_router(ClassroomRouter)
app.include_router(ClassesRouter)
app.include_router(DayTypeRouter)
app.include_router(EducationalCoursesRouter)
app.include_router(YearsGroupsRouter)
app.include_router(YearsGroupsEducationalCoursesRouter)