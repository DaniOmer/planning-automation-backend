from fastapi import APIRouter, Depends, HTTPException
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
