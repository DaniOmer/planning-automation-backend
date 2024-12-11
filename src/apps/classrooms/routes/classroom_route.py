from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

# Import direct des schémas et du service pour éviter les cycles
from src.apps.classrooms.model.classroom_schema import (ClassroomCreate,
                                                        ClassroomResponse)
from src.apps.classrooms.services.classroom_service import ClassroomService
from src.config.database_service import get_db
from src.helpers import TransformHelper

router = APIRouter(prefix="/classrooms")

@router.post("/", response_class=JSONResponse)
async def create_classroom(
    classroom_data: ClassroomCreate,
    session: AsyncSession = Depends(get_db)
):
    try:
        classroom = await ClassroomService.create_classroom(classroom_data, session)
        classroom_dict = TransformHelper.map_to_dict(classroom)
        return ClassroomResponse(**classroom_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_class=JSONResponse)
async def list_classrooms(session: AsyncSession = Depends(get_db)):
    classrooms = await ClassroomService.list_classrooms(session)
    classrooms_dict = [TransformHelper.map_to_dict(classroom) for classroom in classrooms]
    return [ClassroomResponse(**classroom) for classroom in classrooms_dict]

@router.get("/{classroom_id}", response_class=JSONResponse)
async def get_classroom(classroom_id: int, session: AsyncSession = Depends(get_db)):
    try:
        classroom = await ClassroomService.get_classroom_by_id(classroom_id, session)
        classroom_dict = TransformHelper.map_to_dict(classroom)
        return ClassroomResponse(**classroom_dict)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching classroom: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")