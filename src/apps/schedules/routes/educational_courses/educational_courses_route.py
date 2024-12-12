from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database_service import get_db
from src.apps.schedules.model.educational_courses.educational_courses_model import EducationalCourses
from src.apps.schedules.model.educational_courses.educational_courses_schema import EducationalCourseCreate, EducationalCourseResponse
from src.apps.schedules.services.educational_courses.educational_courses_service import EducationalCourseService
from src.apps.schedules.model.years_groups.years_groups_model import YearsGroups
from src.helpers import TransformHelper
from sqlalchemy.future import select
import pandas as pd
import io

router = APIRouter(prefix="/educational_courses", tags=["EducationalCourses"])

@router.post("/create", response_model=EducationalCourseResponse)
async def create_educational_course(
    course_data: EducationalCourseCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        created_course = await EducationalCourseService.create_educational_course(course_data, session)
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
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(YearsGroups).filter(YearsGroups.id == years_group_id))
    years_group = result.scalar_one_or_none()
    if not years_group:
        raise HTTPException(status_code=404, detail="Years group not found")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        required_columns = ["id", "description", "day", "day_type"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}. Expected: {', '.join(required_columns)}")
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns in CSV. Expected: {', '.join(required_columns)}")

        for _, row in df.iterrows():
            course_data = EducationalCourseCreate(
                id=row["id"],
                description=row.get("description", ""),
                day=row.get("day", ""),
                day_type=row.get("day_type", ""),
                years_group_id=years_group_id,
            )
            await EducationalCourseService.create_educational_course(course_data, session)

        return {"detail": "Courses successfully imported from CSV"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")

@router.get("/", response_model=list[EducationalCourseResponse])
async def get_educational_courses(session: AsyncSession = Depends(get_db)):
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
    session: AsyncSession = Depends(get_db)
):
    updated_course = await EducationalCourseService.update_educational_course(course_id, course_data, session)
    if not updated_course:
        raise HTTPException(status_code=404, detail="EducationalCourse not found")
    return EducationalCourseResponse(**TransformHelper.map_to_dict(updated_course))

@router.delete("/{course_id}", response_model=dict)
async def delete_educational_course(course_id: int, session: AsyncSession = Depends(get_db)):
    success = await EducationalCourseService.delete_educational_course(course_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="EducationalCourse not found")
    return {"detail": "EducationalCourse successfully deleted"}