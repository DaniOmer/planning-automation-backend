from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database_service import get_db
from src.apps.schedules.model.day_type.day_type_model import DayType
from src.apps.schedules.model.day_type.day_type_schema import DayTypeCreate, DayTypeResponse
from src.apps.schedules.services.day_type.day_type_service import DayTypeService
from src.helpers import TransformHelper

router = APIRouter(prefix="/day_types")

@router.post("/create", response_model=DayTypeResponse)
async def create_day_type(
    day_type_data: DayTypeCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        created_day_type = await DayTypeService.create_day_type(day_type_data, session)
        day_type_dict = TransformHelper.map_to_dict(created_day_type)
        return DayTypeResponse(**day_type_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/", response_model=list[DayTypeResponse])
async def get_day_types(session: AsyncSession = Depends(get_db)):
    try:
        result = await DayTypeService.get_all_day_types(session)
        return [DayTypeResponse(**TransformHelper.map_to_dict(item)) for item in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{day_type_id}", response_model=DayTypeResponse)
async def get_day_type(day_type_id: int, session: AsyncSession = Depends(get_db)):
    day_type_obj = await DayTypeService.get_day_type_by_id(day_type_id, session)
    if not day_type_obj:
        raise HTTPException(status_code=404, detail="DayType not found")
    return DayTypeResponse(**TransformHelper.map_to_dict(day_type_obj))

@router.put("/{day_type_id}", response_model=DayTypeResponse)
async def update_day_type(
    day_type_id: int, 
    day_type_data: DayTypeCreate, 
    session: AsyncSession = Depends(get_db)
):
    updated_day_type = await DayTypeService.update_day_type(day_type_id, day_type_data, session)
    if not updated_day_type:
        raise HTTPException(status_code=404, detail="DayType not found")
    return DayTypeResponse(**TransformHelper.map_to_dict(updated_day_type))

@router.delete("/{day_type_id}", response_model=dict)
async def delete_day_type(day_type_id: int, session: AsyncSession = Depends(get_db)):
    success = await DayTypeService.delete_day_type(day_type_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="DayType not found")
    return {"detail": "DayType successfully deleted"}