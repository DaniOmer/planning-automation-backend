from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.schedules.model.sessions_subjects.sessions_subjects_schema import (
    SessionSubjectCreate, SessionSubjectResponse, SessionSubjectUpdate)
from src.apps.schedules.services.sessions_subjects.session_subject_service import \
    SessionSubjectService
from src.config.database_service import get_db
from src.helpers.security_helper import SecurityHelper

router = APIRouter(prefix="/sessions-subjects", tags=["SessionsSubjects"])

@router.post("/", response_model=SessionSubjectResponse)
async def create_session_subject(
    data: SessionSubjectCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.create_session_subject(data, session)

@router.get("/{session_subject_id}", response_model=SessionSubjectResponse)
async def get_session_subject(
    session_subject_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.get_session_subject_by_id(session_subject_id, session)

@router.get("/", response_model=list[SessionSubjectResponse])
async def list_session_subjects(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.list_session_subjects(session)

@router.put("/{session_subject_id}", response_model=SessionSubjectResponse)
async def update_session_subject(
    session_subject_id: int,
    data: SessionSubjectUpdate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.update_session_subject(session_subject_id, data, session)

@router.delete("/{session_subject_id}")
async def delete_session_subject(
    session_subject_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.delete_session_subject(session_subject_id, session)


@router.get("/teacher/{teacher_id}", response_model=list[SessionSubjectResponse])
async def get_teacher_sessions(
    teacher_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user)
):
    user_id = int(current_user['sub'])  
    user_role = current_user['role']   

    if user_role == "admin":
        pass 
    elif user_role == "teacher":
        if user_id != teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Teacher cannot access sessions of another teacher."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access these sessions."
        )

    return await SessionSubjectService.get_teacher_sessions(teacher_id, session)

@router.get("/class/{class_id}", response_model=list[SessionSubjectResponse])
async def get_class_sessions(
    class_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.get_class_sessions(class_id, session)

@router.get("/subject/{subject_id}", response_model=list[SessionSubjectResponse])
async def get_subject_sessions(
    subject_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await SessionSubjectService.get_subject_sessions(subject_id, session)