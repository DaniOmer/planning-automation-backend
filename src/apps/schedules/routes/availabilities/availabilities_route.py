from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database_service import get_db
from src.apps.schedules.services.availabilities.availabilities_service import AvailabilityService
from src.apps.schedules.model.availabilities.availabilities_schema import (
    AvailabilityCreateSchema,
    AvailabilityUpdateSchema,
    AvailabilityResponseSchema
)
from src.helpers import SecurityHelper

router = APIRouter(prefix="/availabilities", tags=["Availabilities"])

@router.get("/", response_model=list[AvailabilityResponseSchema])
async def read_availability_by_users_id(
    current_user: dict = Depends(SecurityHelper.get_current_user),
    session: AsyncSession = Depends(get_db)
):
    try:
        user_id = current_user["sub"]
        availability = await AvailabilityService.get_availabilities_by_users_id(session, user_id)
        return availability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=AvailabilityResponseSchema)
async def create_new_availability(
    availability: AvailabilityCreateSchema,
    current_user: dict = Depends(SecurityHelper.get_current_user), 
    session: AsyncSession = Depends(get_db)
):
    try:
        slots = availability.dict().get('slots')
        user_id = current_user.get("sub")
        availability = await AvailabilityService.create_availability(session, slots, user_id)
        return availability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{availability_id}", response_model=AvailabilityResponseSchema)
async def update_existing_availability(
    availability_id: int, 
    availability: AvailabilityUpdateSchema,
    current_user: dict = Depends(SecurityHelper.get_current_user), 
    session: AsyncSession = Depends(get_db)
):
    try:
        slots = availability.dict().get('slots')
        user_id = current_user["sub"]
        updated_availability = await AvailabilityService.update_availability(session, availability_id, slots, user_id)
        return updated_availability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{availability_id}")
async def delete_existing_availability(
    availability_id: int, 
    current_user: dict = Depends(SecurityHelper.get_current_user),
    session: AsyncSession = Depends(get_db)
):
    try:
        await AvailabilityService.delete_availability(session, availability_id)
        return {"message": "Availability deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
