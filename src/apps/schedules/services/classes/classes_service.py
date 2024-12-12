from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.apps.schedules import Classes, ClassCreate

class ClassService:
    
    @staticmethod
    async def create_class(class_data: ClassCreate, session: AsyncSession):
        new_class = Classes(**class_data.dict())
        session.add(new_class)
        await session.commit()
        await session.refresh(new_class)
        return new_class
    
    @staticmethod
    async def get_all_classes(session: AsyncSession):
        result = await session.execute(select(Classes))
        return result.scalars().all()
    
    @staticmethod
    async def get_class_by_id(class_id: int, session: AsyncSession):
        result = await session.execute(
            select(Classes).filter(Classes.id == class_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_class(class_id: int, class_data: ClassCreate, session: AsyncSession):
        class_obj = await ClassService.get_class_by_id(class_id, session)
        if class_obj:
            for key, value in class_data.dict().items():
                setattr(class_obj, key, value)
            await session.commit()
            await session.refresh(class_obj)
            return class_obj
        return None
    
    @staticmethod
    async def delete_class(class_id: int, session: AsyncSession):
        class_obj = await ClassService.get_class_by_id(class_id, session)
        if class_obj:
            await session.delete(class_obj)
            await session.commit()
            return True
        return False