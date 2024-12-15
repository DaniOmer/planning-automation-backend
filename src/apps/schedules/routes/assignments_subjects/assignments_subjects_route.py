from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.schedules.model.assignments_subjects.assignments_subjects_schema import (
    AssignmentSubjectCreate, AssignmentSubjectResponse)
from src.apps.schedules.services.assignments_subjects.assignments_subjects_services import \
    AssignmentsSubjectsService
from src.config.database_service import get_db
from src.helpers import SecurityHelper

router = APIRouter(prefix="/assignments-subjects", tags=["AssignmentsSubjects"])

@router.post("/", response_class=JSONResponse)
async def create_assignment_course(
    data: AssignmentSubjectCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    try:
        return await AssignmentsSubjectsService.create_assignment_course(data, session)
    except HTTPException as e:
        logger.error(f"Error in create_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create assignment course")

@router.get("/", response_class=JSONResponse, response_model=list[AssignmentSubjectResponse])
async def list_assignment_courses(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user)
):
    try:
        return await AssignmentsSubjectsService.list_assignment_courses(session)
    except Exception as e:
        logger.error(f"Unexpected error in list_assignment_courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch assignment courses")

@router.get("/{assignment_id}", response_class=JSONResponse, response_model=AssignmentSubjectResponse)
async def get_assignment_course(
    assignment_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    try:
        return await AssignmentsSubjectsService.get_assignment_course_by_id(assignment_id, session)
    except HTTPException as e:
        logger.error(f"Error in get_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch assignment course")

@router.delete("/{assignment_id}", response_class=JSONResponse)
async def delete_assignment_course(
    assignment_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    try:
        return await AssignmentsSubjectsService.delete_assignment_course(assignment_id, session)
    except HTTPException as e:
        logger.error(f"Error in delete_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in delete_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete assignment course")
    
@router.put("/{assignment_id}", response_class=JSONResponse, response_model=AssignmentSubjectResponse)
async def update_assignment_course(
    assignment_id: int,
    data: AssignmentSubjectCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    try:
        return await AssignmentsSubjectsService.update_assignment_course(assignment_id, data, session)
    except HTTPException as e:
        logger.error(f"Error in update_assignment_course: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in update_assignment_course: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update assignment course")


@router.get("/teacher/{teacher_id}", response_class=JSONResponse, response_model=list[AssignmentSubjectResponse])
async def get_assignments_by_teacher(
    teacher_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user),
):
    """Retrieve all assignments for a specific teacher."""
    try:
        assignments = await AssignmentsSubjectsService.get_assignments_by_teacher(teacher_id, session)
        return assignments
    except HTTPException as e:
        logger.error(f"Error fetching assignments for teacher {teacher_id}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching assignments for teacher {teacher_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch assignments for the specified teacher."
        )
