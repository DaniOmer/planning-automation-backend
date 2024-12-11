from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import JSONResponse

from src.config.database_service import get_db
from src.helpers import TransformHelper
from src.apps.schedules.model.years_groups_educational_courses.years_groups_educational_courses_model import YearsGroupsEducationalCourses
from src.apps.schedules.model.years_groups_educational_courses.years_groups_educational_courses_schema import YearsGroupsEducationalCoursesSchema
from src.apps.schedules.services.years_groups_educational_courses.years_groups_educational_courses_service import YearsGroupsEducationalCoursesService

router = APIRouter(prefix="/years-groups-educational-courses")


@router.post("/", response_class=JSONResponse)
async def create_years_groups_educational_course(
    data: YearsGroupsEducationalCoursesSchema,
    session: AsyncSession = Depends(get_db),
):
    try:
        entry = await YearsGroupsEducationalCoursesService.create_entry(data, session)
        entry_dict = TransformHelper.map_to_dict(entry)
        return JSONResponse(content=entry_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/", response_class=JSONResponse)
async def get_all_years_groups_educational_courses(
    session: AsyncSession = Depends(get_db),
):
    try:
        entries = await YearsGroupsEducationalCoursesService.get_all_entries(session)
        return JSONResponse(
            content=[TransformHelper.map_to_dict(entry) for entry in entries]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/{years_group_id}/{educational_courses_id}", response_class=JSONResponse)
async def get_years_groups_educational_course(
    years_group_id: int,
    educational_courses_id: int,
    session: AsyncSession = Depends(get_db),
):
    try:
        entry = await YearsGroupsEducationalCoursesService.get_entry_by_ids(
            years_group_id, educational_courses_id, session
        )
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return JSONResponse(content=TransformHelper.map_to_dict(entry))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.put("/{years_group_id}/{educational_courses_id}", response_class=JSONResponse)
async def update_years_groups_educational_course(
    years_group_id: int,
    educational_courses_id: int,
    data: YearsGroupsEducationalCoursesSchema,
    session: AsyncSession = Depends(get_db),
):
    try:
        entry = await YearsGroupsEducationalCoursesService.update_entry(
            years_group_id, educational_courses_id, data, session
        )
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return JSONResponse(content=TransformHelper.map_to_dict(entry))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/{years_group_id}/{educational_courses_id}", response_class=JSONResponse)
async def delete_years_groups_educational_course(
    years_group_id: int,
    educational_courses_id: int,
    session: AsyncSession = Depends(get_db),
):
    try:
        success = await YearsGroupsEducationalCoursesService.delete_entry(
            years_group_id, educational_courses_id, session
        )
        if not success:
            raise HTTPException(status_code=404, detail="Entry not found")
        return JSONResponse(content={"detail": "Entry successfully deleted"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")