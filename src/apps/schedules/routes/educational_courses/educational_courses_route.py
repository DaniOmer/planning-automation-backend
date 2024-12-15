import io

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.apps.schedules.model.educational_courses.educational_courses_model import \
    EducationalCourses
from src.apps.schedules.model.educational_courses.educational_courses_schema import (
    EducationalCourseCreate, EducationalCourseResponse)
from src.apps.schedules.model.years_groups.years_groups_model import \
    YearsGroups
from src.apps.schedules.model.years_groups_educational_courses.years_groups_educational_courses_model import \
    YearsGroupsEducationalCourses
from src.apps.schedules.services.educational_courses.educational_courses_service import \
    EducationalCourseService
from src.config.database_service import get_db
from src.helpers import SecurityHelper, TransformHelper
from src.utils.csv_utils import import_csv

router = APIRouter(prefix="/educational_courses", tags=["EducationalCourses"])

@router.post("/create", response_model=EducationalCourseResponse)
async def create_educational_course(
    course_data: EducationalCourseCreate, 
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    try:
        created_course = await EducationalCourseService.get_or_create_educational_course(course_data, session)
        course_dict = TransformHelper.map_to_dict(created_course)
        return EducationalCourseResponse(**course_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.post("/import/{years_group_id}", response_model=dict)
async def import_educational_courses(
    years_group_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    result = await session.execute(select(YearsGroups).filter(YearsGroups.id == years_group_id))
    years_group = result.scalar_one_or_none()
    if not years_group:
        raise HTTPException(status_code=404, detail="Years group not found")

    required_columns = ["id", "description", "day", "day_type"]

    async def link_to_years_groups(course, row, session):
        years_groups_course_data = {
            "educational_courses_id": course.id,
            "years_group_id": years_group_id,
            "day_type": row.get("day_type")
        }
        await session.execute(
            insert(YearsGroupsEducationalCourses).values(years_groups_course_data)
        )
        await session.commit()

    try:
        return await import_csv(
            file=file,
            session=session,
            entity_class=EducationalCourseCreate,
            create_service=EducationalCourseService.create_educational_course,
            required_columns=required_columns,
            post_create_action=link_to_years_groups,
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required column: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")

@router.get("/", response_model=list[EducationalCourseResponse])
async def get_educational_courses(
    session: AsyncSession = Depends(get_db),
    current_user= Depends(SecurityHelper.get_current_user)
                                  ):
    try:
        result = await EducationalCourseService.get_all_educational_courses(session)
        return [EducationalCourseResponse(**TransformHelper.map_to_dict(item)) for item in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{course_id}", response_model=EducationalCourseResponse)
async def get_educational_course(course_id: int, session: AsyncSession = Depends(get_db)):
    course_obj = await EducationalCourseService.get_educational_course_by_id(course_id, session)
    if not course_obj:
        raise HTTPException(status_code=404, detail="EducationalCourse not found")
    return EducationalCourseResponse(**TransformHelper.map_to_dict(course_obj))

@router.put("/{course_id}", response_model=EducationalCourseResponse)
async def update_educational_course(
    course_id: int, 
    course_data: EducationalCourseCreate, 
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    updated_course = await EducationalCourseService.update_educational_course(course_id, course_data, session)
    if not updated_course:
        raise HTTPException(status_code=404, detail="EducationalCourse not found")
    return EducationalCourseResponse(**TransformHelper.map_to_dict(updated_course))

@router.delete("/{course_id}", response_model=dict)
async def delete_educational_course(
    course_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    success = await EducationalCourseService.delete_educational_course(course_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="EducationalCourse not found")
    return {"detail": "EducationalCourse successfully deleted"}