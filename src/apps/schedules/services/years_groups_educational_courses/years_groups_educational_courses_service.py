from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.apps.schedules import YearsGroupsEducationalCourses

class YearsGroupsEducationalCoursesService:
    @staticmethod
    async def create_entry(data, session: AsyncSession):
        entry = YearsGroupsEducationalCourses(**data.dict())
        session.add(entry)
        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def get_all_entries(session: AsyncSession):
        result = await session.execute(select(YearsGroupsEducationalCourses))
        return result.scalars().all()

    @staticmethod
    async def get_entry_by_ids(years_group_id, educational_courses_id, session: AsyncSession):
        result = await session.execute(
            select(YearsGroupsEducationalCourses).filter(
                YearsGroupsEducationalCourses.years_group_id == years_group_id,
                YearsGroupsEducationalCourses.educational_courses_id == educational_courses_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_entry(years_group_id, educational_courses_id, data, session: AsyncSession):
        entry = await YearsGroupsEducationalCoursesService.get_entry_by_ids(
            years_group_id, educational_courses_id, session
        )
        if entry:
            for key, value in data.dict().items():
                setattr(entry, key, value)
            await session.commit()
            await session.refresh(entry)
        return entry

    @staticmethod
    async def delete_entry(years_group_id, educational_courses_id, session: AsyncSession):
        entry = await YearsGroupsEducationalCoursesService.get_entry_by_ids(
            years_group_id, educational_courses_id, session
        )
        if entry:
            await session.delete(entry)
            await session.commit()
            return True
        return False
