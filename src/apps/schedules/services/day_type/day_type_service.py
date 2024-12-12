from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.apps.schedules import DayType, DayTypeCreate

class DayTypeService:
    
    @staticmethod
    async def create_day_type(day_type_data: DayTypeCreate, session: AsyncSession):
        new_day_type = DayType(**day_type_data.dict())
        session.add(new_day_type)
        await session.commit()
        await session.refresh(new_day_type)
        return new_day_type
    
    @staticmethod
    async def get_all_day_types(session: AsyncSession):
        result = await session.execute(select(DayType))
        return result.scalars().all()
    
    @staticmethod
    async def get_day_type_by_id(day_type_id: int, session: AsyncSession):
        result = await session.execute(
            select(DayType).filter(DayType.id == day_type_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_day_type(day_type_id: int, day_type_data: DayTypeCreate, session: AsyncSession):
        day_type_obj = await DayTypeService.get_day_type_by_id(day_type_id, session)
        if day_type_obj:
            for key, value in day_type_data.dict().items():
                setattr(day_type_obj, key, value)
            await session.commit()
            await session.refresh(day_type_obj)
            return day_type_obj
        return None
    
    @staticmethod
    async def delete_day_type(day_type_id: int, session: AsyncSession):
        day_type_obj = await DayTypeService.get_day_type_by_id(day_type_id, session)
        if day_type_obj:
            await session.delete(day_type_obj)
            await session.commit()
            return True
        return False