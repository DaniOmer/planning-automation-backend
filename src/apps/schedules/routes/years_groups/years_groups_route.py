from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database_service import get_db
from src.apps.schedules.model.years_groups.years_groups_model import YearsGroups
from src.apps.schedules.model.years_groups.years_groups_schema import YearsGroupCreate, YearsGroupResponse
from src.apps.schedules.services.years_groups.years_groups_service import YearsGroupService
from src.helpers import TransformHelper

router = APIRouter(prefix="/years_groups")

@router.post("/create", response_model=YearsGroupResponse, tags=["YearsGroupResponse"])
async def create_years_group(
    group_data: YearsGroupCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        created_group = await YearsGroupService.create_years_group(group_data, session)
        group_dict = TransformHelper.map_to_dict(created_group)
        return YearsGroupResponse(**group_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/", response_model=list[YearsGroupResponse])
async def get_years_groups(session: AsyncSession = Depends(get_db)):
    try:
        result = await YearsGroupService.get_all_years_groups(session)
        return [YearsGroupResponse(**TransformHelper.map_to_dict(item)) for item in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{group_id}", response_model=YearsGroupResponse)
async def get_years_group(group_id: int, session: AsyncSession = Depends(get_db)):
    group_obj = await YearsGroupService.get_years_group_by_id(group_id, session)
    if not group_obj:
        raise HTTPException(status_code=404, detail="YearsGroup not found")
    return YearsGroupResponse(**TransformHelper.map_to_dict(group_obj))

@router.put("/{group_id}", response_model=YearsGroupResponse)
async def update_years_group(
    group_id: int, 
    group_data: YearsGroupCreate, 
    session: AsyncSession = Depends(get_db)
):
    updated_group = await YearsGroupService.update_years_group(group_id, group_data, session)
    if not updated_group:
        raise HTTPException(status_code=404, detail="YearsGroup not found")
    return YearsGroupResponse(**TransformHelper.map_to_dict(updated_group))

@router.delete("/{group_id}", response_model=dict)
async def delete_years_group(group_id: int, session: AsyncSession = Depends(get_db)):
    success = await YearsGroupService.delete_years_group(group_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="YearsGroup not found")
    return {"detail": "YearsGroup successfully deleted"}