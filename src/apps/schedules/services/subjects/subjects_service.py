from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.schedules.model.subjects.subjects_model import Subjects
from src.apps.schedules.model.subjects.subjects_schema import SubjectCreate, SubjectUpdate
from fastapi import HTTPException

def validate_subject_period(start_at, end_at, hourly_volume):
    if not start_at or not end_at:
        raise HTTPException(status_code=400, detail="Les dates de début et de fin doivent être fournies.")

    total_days = (end_at - start_at).days + 1
    max_hours_per_day = 12
    total_available_hours = total_days * max_hours_per_day

    if hourly_volume > total_available_hours:
        raise HTTPException(status_code=400, detail="La période entre la date de début et de fin n'est pas suffisante pour accueillir le volume horaire de la matière. Max 12h/j")

async def get_subjects(db: AsyncSession):
    result = await db.execute(select(Subjects))
    return result.scalars().all()

async def get_subject_by_id(db: AsyncSession, subject_id: int):
    result = await db.execute(select(Subjects).where(Subjects.id == subject_id))
    return result.scalars().first()

async def create_subject(db: AsyncSession, subject: SubjectCreate):
    validate_subject_period(subject.start_at, subject.end_at, subject.hourly_volume)

    db_subject = Subjects(**subject.dict())
    db.add(db_subject)
    await db.commit()
    await db.refresh(db_subject)
    return db_subject

async def update_subject(db: AsyncSession, subject_id: int, subject: SubjectUpdate):
    db_subject = await get_subject_by_id(db, subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Le sujet avec cet ID n'a pas été trouvé.")

    start_at = subject.start_at or db_subject.start_at
    end_at = subject.end_at or db_subject.end_at
    hourly_volume = subject.hourly_volume or db_subject.hourly_volume

    validate_subject_period(start_at, end_at, hourly_volume)

    for key, value in subject.dict(exclude_unset=True).items():
        setattr(db_subject, key, value)
    await db.commit()
    await db.refresh(db_subject)
    return db_subject

async def delete_subject(db: AsyncSession, subject_id: int):
    db_subject = await get_subject_by_id(db, subject_id)
    if db_subject:
        await db.delete(db_subject)
        await db.commit()
    return db_subject
