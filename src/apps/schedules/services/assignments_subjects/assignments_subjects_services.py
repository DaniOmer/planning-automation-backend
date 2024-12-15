from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import \
    AssignmentSubject
from src.apps.schedules.model.assignments_subjects.assignments_subjects_schema import \
    AssignmentSubjectCreate
from src.apps.schedules.model.classes.classes_model import Classes
from src.apps.schedules.model.subjects.subjects_model import Subjects
from src.apps.users.model.user.user_model import User
from src.helpers import ValidationHelper


class AssignmentsSubjectsService:
    """Service for operations related to assignments_courses"""

    @staticmethod
    async def create_assignment_course(data: AssignmentSubjectCreate, session: AsyncSession):
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
            await ValidationHelper.validate_id(Subjects, data.subjects_id, session, "Subject")

            assignment_data = data.model_dump()
            logger.debug(f"Cleaned data for AssignmentSubject creation: {assignment_data}")

            assignment_course = AssignmentSubject(**assignment_data)
            session.add(assignment_course)
            await session.commit()
            await session.refresh(assignment_course)
            logger.info(f"AssignmentSubject created successfully with ID: {assignment_course.id}")
            return assignment_course

        except IntegrityError as e:
            if 'uq_classes_subjects' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
               detail=(
                            "This class is already assigned to another teacher for the selected subject. "
                            "Please choose a different combination, as only one teacher can be assigned per class-subject pair."
                        )

                )
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    @staticmethod
    async def get_assignment_course_by_id(assignment_id: int, session: AsyncSession):
        """Fetch assignment course by ID with related entities"""
        try:
            query = select(AssignmentSubject).options(
                joinedload(AssignmentSubject.class_info),
                joinedload(AssignmentSubject.subject_info),
                joinedload(AssignmentSubject.user_info)
            ).where(AssignmentSubject.id == assignment_id)

            result = await session.execute(query)
            assignment_course = result.scalar_one_or_none()

            if not assignment_course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"AssignmentSubject with ID {assignment_id} not found"
                )
            logger.info(f"Fetched AssignmentSubject with ID: {assignment_id}")
            return assignment_course
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error fetching AssignmentSubject: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch assignment course"
            )

    @staticmethod
    async def list_assignment_courses(session: AsyncSession):
        """List all assignment courses with related entities"""
        try:
            query = select(AssignmentSubject).options(
                joinedload(AssignmentSubject.class_info),
                joinedload(AssignmentSubject.subject_info),
                joinedload(AssignmentSubject.user_info)
            )
            result = await session.execute(query)
            assignments = result.scalars().all()
            logger.info(f"Fetched {len(assignments)} AssignmentSubjects")
            return assignments
        except Exception as e:
            logger.error(f"Unexpected error listing AssignmentSubjects: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to list assignment courses"
            )

    @staticmethod
    async def update_assignment_course(assignment_id: int, data: AssignmentSubjectCreate, session: AsyncSession):
        """Update an existing assignment course"""
        try:
            assignment_course = await AssignmentsSubjectsService.get_assignment_course_by_id(assignment_id, session)

            await ValidationHelper.validate_id(User, data.users_id, session, "User")
            await ValidationHelper.validate_id(Classes, data.classes_id, session, "Class")
            await ValidationHelper.validate_id(Subjects, data.subjects_id, session, "Subject")

            assignment_course.classes_id = data.classes_id
            assignment_course.subjects_id = data.subjects_id
            assignment_course.users_id = data.users_id
            assignment_course.url_online = data.url_online

            await session.commit()
            await session.refresh(assignment_course)
            logger.info(f"AssignmentSubject with ID {assignment_id} updated successfully")
            return assignment_course
        except HTTPException as e:
            logger.error(f"HTTP Exception during update: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error updating AssignmentSubject: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update assignment course"
            )

    @staticmethod
    async def delete_assignment_course(assignment_id: int, session: AsyncSession):
        """Delete an assignment course by ID"""
        try:
            assignment_course = await AssignmentsSubjectsService.get_assignment_course_by_id(assignment_id, session)
            await session.delete(assignment_course)
            await session.commit()
            logger.info(f"AssignmentSubject with ID {assignment_id} deleted successfully")
            return {"detail": "Assignment deleted successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error deleting AssignmentSubject: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete assignment course"
            )
            
    @staticmethod
    async def get_assignments_by_teacher(teacher_id: int, session: AsyncSession):
        """Fetch all assignment subjects for a given teacher by user_id."""
        try:
            query = select(AssignmentSubject).options(
                joinedload(AssignmentSubject.class_info),
                joinedload(AssignmentSubject.subject_info),
                joinedload(AssignmentSubject.user_info)
            ).where(AssignmentSubject.users_id == teacher_id)

            result = await session.execute(query)
            assignments = result.scalars().all()

            if not assignments:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No assignments found for teacher with ID {teacher_id}."
                )

            logger.info(f"Fetched {len(assignments)} assignments for teacher ID: {teacher_id}")
            return assignments
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error fetching assignments for teacher ID {teacher_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch assignments for the specified teacher."
            )

