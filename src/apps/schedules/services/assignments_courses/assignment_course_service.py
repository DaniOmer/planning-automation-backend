from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.schedules import Classes, Subjects
from src.apps.schedules.model.assignments_courses.assignment_course_model import \
    AssignmentCourse
from src.apps.schedules.model.assignments_courses.assignment_course_schema import \
    AssignmentCourseCreate
from src.apps.users.model.user_model import User
from src.helpers import ValidationHelper


class AssignmentCourseService:
    """Service for operations related to assignments_courses"""

    @staticmethod
    async def create_assignment_course(data: AssignmentCourseCreate, session: AsyncSession):
        """Create a new assignment course"""
        try:
           
            user = await ValidationHelper.validate_id(User, data.users_id, session, "User")
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {data.users_id} not found"
                )
            if user.role != "teacher":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only users with the role 'teacher' can be assigned to a course"
                )

            await ValidationHelper.validate_id(Classes, data.classes_id, session, "Class")
            await ValidationHelper.validate_id(Subjects, data.courses_id, session, "Subject")

            assignment_data = data.model_dump()
            logger.debug(f"Cleaned data for AssignmentCourse creation: {assignment_data}")

            assignment_course = AssignmentCourse(**assignment_data)
            session.add(assignment_course)
            await session.commit()
            await session.refresh(assignment_course)
            logger.info(f"AssignmentCourse created successfully with ID: {assignment_course.id}")
            return assignment_course

        except HTTPException as e:
            logger.error(f"HTTP Exception during creation: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error creating AssignmentCourse: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create assignment course"
            )

    @staticmethod
    async def get_assignment_course_by_id(assignment_id: int, session: AsyncSession):
        """Fetch assignment course by ID with related entities"""
        try:
            query = select(AssignmentCourse).options(
                joinedload(AssignmentCourse.class_info),
                joinedload(AssignmentCourse.course_info),
                joinedload(AssignmentCourse.user_info)
            ).where(AssignmentCourse.id == assignment_id)

            result = await session.execute(query)
            assignment_course = result.scalar_one_or_none()

            if not assignment_course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"AssignmentCourse with ID {assignment_id} not found"
                )
            logger.info(f"Fetched AssignmentCourse with ID: {assignment_id}")
            return assignment_course
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error fetching AssignmentCourse: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch assignment course"
            )

    @staticmethod
    async def list_assignment_courses(session: AsyncSession):
        """List all assignment courses with related entities"""
        try:
            query = select(AssignmentCourse).options(
                joinedload(AssignmentCourse.class_info),
                joinedload(AssignmentCourse.course_info),
                joinedload(AssignmentCourse.user_info)
            )
            result = await session.execute(query)
            assignments = result.scalars().all()
            logger.info(f"Fetched {len(assignments)} AssignmentCourses")
            return assignments
        except Exception as e:
            logger.error(f"Unexpected error listing AssignmentCourses: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to list assignment courses"
            )

    @staticmethod
    async def update_assignment_course(assignment_id: int, data: AssignmentCourseCreate, session: AsyncSession):
        """Update an existing assignment course"""
        try:
            assignment_course = await AssignmentCourseService.get_assignment_course_by_id(assignment_id, session)

            await ValidationHelper.validate_id(User, data.users_id, session, "User")
            await ValidationHelper.validate_id(Classes, data.classes_id, session, "Class")
            await ValidationHelper.validate_id(Subjects, data.courses_id, session, "Subject")

            assignment_course.classes_id = data.classes_id
            assignment_course.courses_id = data.courses_id
            assignment_course.users_id = data.users_id
            assignment_course.url_online = data.url_online

            await session.commit()
            await session.refresh(assignment_course)
            logger.info(f"AssignmentCourse with ID {assignment_id} updated successfully")
            return assignment_course
        except HTTPException as e:
            logger.error(f"HTTP Exception during update: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error updating AssignmentCourse: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update assignment course"
            )

    @staticmethod
    async def delete_assignment_course(assignment_id: int, session: AsyncSession):
        """Delete an assignment course by ID"""
        try:
            assignment_course = await AssignmentCourseService.get_assignment_course_by_id(assignment_id, session)
            await session.delete(assignment_course)
            await session.commit()
            logger.info(f"AssignmentCourse with ID {assignment_id} deleted successfully")
            return {"detail": "Assignment deleted successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error deleting AssignmentCourse: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete assignment course"
            )
