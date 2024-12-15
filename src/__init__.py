from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import *
from src.apps.classrooms import ClassroomRouter
from src.apps.schedules import (AssignmentSubjectsRouter, AvailabilitiesRouter,
                                ClassesRouter,
                                SessionSubjectsRouter, SubjectsRouter,
                                YearsGroupsEducationalCoursesRouter,
                                YearsGroupsRouter, AiRouter)
from src.apps.users import InvitationRouter, UserRouter

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(UserRouter)
app.include_router(InvitationRouter)
app.include_router(ClassroomRouter)
app.include_router(ClassesRouter)
app.include_router(YearsGroupsRouter)
app.include_router(YearsGroupsEducationalCoursesRouter)
app.include_router(AvailabilitiesRouter)
app.include_router(SubjectsRouter)
app.include_router(AssignmentSubjectsRouter)
app.include_router(SessionSubjectsRouter)
app.include_router(AiRouter)
