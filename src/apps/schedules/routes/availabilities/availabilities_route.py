from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database_service import get_db
from src.apps.schedules.services.availabilities.availabilities_service import (
    get_availabilities,
    get_availabilities_by_users_id,
    create_availability,
    update_availability,
    delete_availability
)
from src.apps.schedules.model.availabilities.availabilities_schema import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse
)

router = APIRouter(prefix="/availabilities")

@router.get("/", response_model=list[AvailabilityResponse])
async def read_availabilities(db: AsyncSession = Depends(get_db)):
    return await get_availabilities(db)

@router.get("/user/{users_id}", response_model=list[AvailabilityResponse])
async def read_availability_by_users_id(users_id: int, db: AsyncSession = Depends(get_db)):
    availability = await get_availabilities_by_users_id(db, users_id)
    if not availability:
        raise HTTPException(status_code=404, detail="No availabilities found for this user")
    return availability

@router.post("/", response_model=AvailabilityResponse)
async def create_new_availability(availability: AvailabilityCreate, db: AsyncSession = Depends(get_db)):
    return await create_availability(db, availability)

@router.put("/{availability_id}", response_model=AvailabilityResponse)
async def update_existing_availability(availability_id: int, availability: AvailabilityUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_availability(db, availability_id, availability)
    if not updated:
        raise HTTPException(status_code=404, detail="Availability not found")
    return updated

@router.delete("/{availability_id}")
async def delete_existing_availability(availability_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_availability(db, availability_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}
