from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.apps.schedules import EducationalCourses, EducationalCourseCreate

class EducationalCourseService:
    
    @staticmethod
    async def create_educational_course(course_data: EducationalCourseCreate, session: AsyncSession):
        new_course = EducationalCourses(**course_data.dict())
        session.add(new_course)
        await session.commit()
        await session.refresh(new_course)
        return new_course
    
    @staticmethod
    async def get_all_educational_courses(session: AsyncSession):
        result = await session.execute(select(EducationalCourses))
        return result.scalars().all()
    
    @staticmethod
    async def get_educational_course_by_id(course_id: int, session: AsyncSession):
        result = await session.execute(
            select(EducationalCourses).filter(EducationalCourses.id == course_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_educational_course(course_id: int, course_data: EducationalCourseCreate, session: AsyncSession):
        course_obj = await EducationalCourseService.get_educational_course_by_id(course_id, session)
        if course_obj:
            for key, value in course_data.dict().items():
                setattr(course_obj, key, value)
            await session.commit()
            await session.refresh(course_obj)
            return course_obj
        return None
    
    @staticmethod
    async def delete_educational_course(course_id: int, session: AsyncSession):
        course_obj = await EducationalCourseService.get_educational_course_by_id(course_id, session)
        if course_obj:
            await session.delete(course_obj)
            await session.commit()
            return True
        return False