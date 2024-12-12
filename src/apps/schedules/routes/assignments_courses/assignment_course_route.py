from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.schedules.model.assignments_courses.assignment_course_schema import (
    AssignmentCourseCreate, AssignmentCourseResponse)
from src.apps.schedules.services.assignments_courses.assignment_course_service import \
    AssignmentCourseService
from src.config.database_service import get_db

router = APIRouter(prefix="/assignments-courses", tags=["AssignmentsCourses"])

@router.post("/", response_class=JSONResponse, response_model=AssignmentCourseResponse)
async def create_assignment_course(
    data: AssignmentCourseCreate,
    session: AsyncSession = Depends(get_db)
):
    try:
        return await AssignmentCourseService.create_assignment_course(data, session)
    except HTTPException as e:
        logger.error(f"Error in create_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create assignment course")

@router.get("/", response_class=JSONResponse, response_model=list[AssignmentCourseResponse])
async def list_assignment_courses(session: AsyncSession = Depends(get_db)):
    try:
        return await AssignmentCourseService.list_assignment_courses(session)
    except Exception as e:
        logger.error(f"Unexpected error in list_assignment_courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch assignment courses")

@router.get("/{assignment_id}", response_class=JSONResponse, response_model=AssignmentCourseResponse)
async def get_assignment_course(assignment_id: int, session: AsyncSession = Depends(get_db)):
    try:
        return await AssignmentCourseService.get_assignment_course_by_id(assignment_id, session)
    except HTTPException as e:
        logger.error(f"Error in get_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch assignment course")

@router.delete("/{assignment_id}", response_class=JSONResponse)
async def delete_assignment_course(assignment_id: int, session: AsyncSession = Depends(get_db)):
    try:
        return await AssignmentCourseService.delete_assignment_course(assignment_id, session)
    except HTTPException as e:
        logger.error(f"Error in delete_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in delete_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete assignment course")
    
@router.put("/{assignment_id}", response_class=JSONResponse, response_model=AssignmentCourseResponse)
async def update_assignment_course(
    assignment_id: int,
    data: AssignmentCourseCreate,
    session: AsyncSession = Depends(get_db)
):
    try:
        return await AssignmentCourseService.update_assignment_course(assignment_id, data, session)
    except HTTPException as e:
        logger.error(f"Error in update_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in update_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update assignment course")

