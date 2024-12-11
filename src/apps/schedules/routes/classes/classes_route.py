from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.config.database_service import get_db
from src.apps.schedules.model.classes.classes_model import Classes
from src.apps.schedules.model.classes.classes_schema import ClassCreate, ClassResponse
from src.apps.schedules.services.classes.classes_service import ClassService
from src.helpers import TransformHelper

router = APIRouter(prefix="/classes")

@router.post("/create", response_model=ClassResponse)
async def create_class(
    class_data: ClassCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        # Création de la classe via le service
        created_class = await ClassService.create_class(class_data, session)
        class_dict = TransformHelper.map_to_dict(created_class)
        return ClassResponse(**class_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/", response_model=list[ClassResponse])
async def get_classes(session: AsyncSession = Depends(get_db)):
    try:
        result = await ClassService.get_all_classes(session)
        return [ClassResponse(**TransformHelper.map_to_dict(item)) for item in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{class_id}", response_model=ClassResponse)
async def get_class(class_id: int, session: AsyncSession = Depends(get_db)):
    try:
        class_obj = await ClassService.get_class_by_id(class_id, session)
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")
        return ClassResponse(**TransformHelper.map_to_dict(class_obj))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.put("/{class_id}", response_model=ClassResponse)
async def update_class(
    class_id: int, 
    class_data: ClassCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        updated_class = await ClassService.update_class(class_id, class_data, session)
        if not updated_class:
            raise HTTPException(status_code=404, detail="Class not found")
        return ClassResponse(**TransformHelper.map_to_dict(updated_class))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.delete("/{class_id}", response_model=dict)
async def delete_class(class_id: int, session: AsyncSession = Depends(get_db)):
    try:
        success = await ClassService.delete_class(class_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="Class not found")
        return {"detail": "Class successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
