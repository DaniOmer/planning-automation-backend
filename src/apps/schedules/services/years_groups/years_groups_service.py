from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.apps.schedules import YearsGroups, YearsGroupCreate

class YearsGroupService:
    
    @staticmethod
    async def create_years_group(group_data: YearsGroupCreate, session: AsyncSession):
        new_group = YearsGroups(**group_data.dict())
        session.add(new_group)
        await session.commit()
        await session.refresh(new_group)
        return new_group
    
    @staticmethod
    async def get_all_years_groups(session: AsyncSession):
        result = await session.execute(select(YearsGroups))
        return result.scalars().all()
    
    @staticmethod
    async def get_years_group_by_id(group_id: int, session: AsyncSession):
        result = await session.execute(
            select(YearsGroups).filter(YearsGroups.id == group_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_years_group(group_id: int, group_data: YearsGroupCreate, session: AsyncSession):
        group_obj = await YearsGroupService.get_years_group_by_id(group_id, session)
        if group_obj:
            for key, value in group_data.dict().items():
                setattr(group_obj, key, value)
            await session.commit()
            await session.refresh(group_obj)
            return group_obj
        return None
    
    @staticmethod
    async def delete_years_group(group_id: int, session: AsyncSession):
        group_obj = await YearsGroupService.get_years_group_by_id(group_id, session)
        if group_obj:
            await session.delete(group_obj)
            await session.commit()
            return True
        return False