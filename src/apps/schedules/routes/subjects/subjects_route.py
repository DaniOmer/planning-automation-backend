from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.schedules.model.subjects.subjects_schema import (SubjectCreate,
                                                               SubjectResponse,
                                                               SubjectUpdate)
from src.apps.schedules.services.subjects.subjects_service import (
    create_subject, delete_subject, get_subject_by_id, get_subjects,
    update_subject)
from src.config.database_service import get_db
from src.helpers.security_helper import SecurityHelper

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("/", response_model=list[SubjectResponse])
async def read_subjects(db: AsyncSession = Depends(get_db)):
    return await get_subjects(db)

@router.get("/{subject_id}", response_model=SubjectResponse)
async def read_subject(subject_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(SecurityHelper.get_current_user)):
    subject = await get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.post("/", response_model=SubjectResponse)
async def create_new_subject(
    subject: SubjectCreate, 
    db: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    return await create_subject(db, subject)

@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_existing_subject(
    subject_id: int, 
    subject: SubjectUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    updated = await update_subject(db, subject_id, subject)
    if not updated:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated

@router.delete("/{subject_id}")
async def delete_existing_subject(
    subject_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin"))
):
    deleted = await delete_subject(db, subject_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}
