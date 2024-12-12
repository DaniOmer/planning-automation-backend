from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.schedules.model.subjects.subjects_model import Subjects
from src.apps.schedules.model.subjects.subjects_schema import SubjectCreate, SubjectUpdate

async def get_subjects(db: AsyncSession):
    result = await db.execute(select(Subjects))
    return result.scalars().all()

async def get_subject_by_id(db: AsyncSession, subject_id: int):
    result = await db.execute(select(Subjects).where(Subjects.id == subject_id))
    return result.scalars().first()

async def create_subject(db: AsyncSession, subject: SubjectCreate):
    db_subject = Subjects(**subject.dict())
    db.add(db_subject)
    await db.commit()
    await db.refresh(db_subject)
    return db_subject

async def update_subject(db: AsyncSession, subject_id: int, subject: SubjectUpdate):
    db_subject = await get_subject_by_id(db, subject_id)
    if not db_subject:
        return None
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
