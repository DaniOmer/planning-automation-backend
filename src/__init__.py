from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import *
from src.apps.users import UserRouter, InvitationRouter
from src.apps.classrooms import ClassroomRouter

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
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

# Routers
app.include_router(UserRouter)
app.include_router(InvitationRouter)
app.include_router(ClassroomRouter)