from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.schedules.model.availabilities.availabilities_model import Availabilities
from src.apps.schedules.model.availabilities.availabilities_schema import AvailabilityCreate, AvailabilityUpdate
from src.apps.users.model.user.user_model import User

async def get_availabilities(db: AsyncSession):
    result = await db.execute(select(Availabilities))
    return result.scalars().all()

async def get_availabilities_by_users_id(db: AsyncSession, users_id: int):
    result = await db.execute(select(Availabilities).where(Availabilities.users_id == users_id))
    return result.scalars().all()

async def verify_user_exists(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    if not result.scalar():
        raise ValueError(f"User with id {user_id} does not exist")

async def create_availability(db: AsyncSession, availability: AvailabilityCreate):
    await verify_user_exists(db, availability.users_id)

    db_availability = Availabilities(**availability.dict())
    db.add(db_availability)
    await db.commit()
    await db.refresh(db_availability)
    return db_availability


async def get_availability_by_id(db: AsyncSession, availability_id: int):
    result = await db.execute(select(Availabilities).where(Availabilities.id == availability_id))
    return result.scalars().first()

async def update_availability(db: AsyncSession, availability_id: int, availability: AvailabilityUpdate):
    db_availability = await get_availability_by_id(db, availability_id)
    if not db_availability:
        return None
    
    if availability.users_id is not None and availability.users_id != db_availability.users_id:
        await verify_user_exists(db, availability.users_id)

    for key, value in availability.dict(exclude_unset=True).items():
        setattr(db_availability, key, value)
    await db.commit()
    await db.refresh(db_availability)
    return db_availability


async def delete_availability(db: AsyncSession, availability_id: int):
    db_availability = await get_availability_by_id(db, availability_id)
    if db_availability:
        await db.delete(db_availability)
        await db.commit()
    return db_availability
