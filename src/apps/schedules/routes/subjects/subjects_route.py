from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database_service import get_db
from src.apps.schedules.services.subjects.subjects_service import (
    get_subjects,
    get_subject_by_id,
    create_subject,
    update_subject,
    delete_subject
)
from src.apps.schedules.model.subjects.subjects_schema import SubjectCreate, SubjectUpdate, SubjectResponse

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("/", response_model=list[SubjectResponse])
async def read_subjects(db: AsyncSession = Depends(get_db)):
    return await get_subjects(db)

@router.get("/{subject_id}", response_model=SubjectResponse)
async def read_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    subject = await get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.post("/", response_model=SubjectResponse)
async def create_new_subject(subject: SubjectCreate, db: AsyncSession = Depends(get_db)):
    return await create_subject(db, subject)

@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_existing_subject(subject_id: int, subject: SubjectUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_subject(db, subject_id, subject)
    if not updated:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated

@router.delete("/{subject_id}")
async def delete_existing_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_subject(db, subject_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}
