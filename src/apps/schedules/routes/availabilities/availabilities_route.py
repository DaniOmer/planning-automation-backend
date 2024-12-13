from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.schedules.model.availabilities.availabilities_schema import (
    AvailabilityCreate, AvailabilityResponse, AvailabilityUpdate)
from src.apps.schedules.services.availabilities.availabilities_service import (
    create_availability, delete_availability, get_availabilities,
    get_availabilities_by_users_id, update_availability)
from src.config.database_service import get_db
from src.helpers import SecurityHelper

router = APIRouter(prefix="/availabilities")

@router.get("/", response_model=list[AvailabilityResponse])
async def read_availabilities(db: AsyncSession = Depends(get_db),
                              current_user=Depends(SecurityHelper.get_current_user)):
    return await get_availabilities(db)

@router.get("/user/{users_id}", response_model=list[AvailabilityResponse])
async def read_availability_by_users_id(users_id: int, db: AsyncSession = Depends(get_db),
                                        current_user=Depends(SecurityHelper.get_current_user)):
    availability = await get_availabilities_by_users_id(db, users_id)
    if not availability:
        raise HTTPException(status_code=404, detail="No availabilities found for this user")
    return availability

@router.post("/", response_model=AvailabilityResponse)
async def create_new_availability(
    availability: AvailabilityCreate, 
    db: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user)
):
    try:
        return await create_availability(db, availability)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{availability_id}", response_model=AvailabilityResponse)
async def update_existing_availability(
    availability_id: int, 
    availability: AvailabilityUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user)
):
    try:
        updated = await update_availability(db, availability_id, availability)
        if not updated:
            raise HTTPException(status_code=404, detail="Availability not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{availability_id}")
async def delete_existing_availability(
    availability_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user)
):
    deleted = await delete_availability(db, availability_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}
