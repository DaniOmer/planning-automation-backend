from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.apps.classrooms.model.classroom_model import Classroom
from src.apps.classrooms.model.classroom_schema import ClassroomCreate


class ClassroomService:
    """Service for operations related to classrooms"""

    @staticmethod
    async def create_classroom(classroom_data: ClassroomCreate, session: AsyncSession):
        try:
            classroom = Classroom(
                name=classroom_data.name,
                capacity=classroom_data.capacity,
            )
            session.add(classroom)
            await session.commit()

            logger.info(f"Classroom created successfully with name: {classroom.name}")
            return classroom
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    @staticmethod
    async def get_classroom_by_id(classroom_id: int, session: AsyncSession):
        query = select(Classroom).where(Classroom.id == classroom_id)
        result = await session.execute(query)
        classroom = result.scalar_one_or_none()
        if not classroom:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")
        return classroom
    
    @staticmethod
    async def list_classrooms(session: AsyncSession):
        query = select(Classroom)
        result = await session.execute(query)
        classrooms = result.scalars().all()
        return classrooms
