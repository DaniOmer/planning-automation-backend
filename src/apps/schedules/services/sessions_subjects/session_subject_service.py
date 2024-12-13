from datetime import datetime

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.classrooms.model.classroom_model import Classroom
from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import \
    AssignmentSubject
from src.apps.schedules.model.sessions_subjects.sessions_subjects_model import \
    SessionSubject
from src.apps.schedules.model.sessions_subjects.sessions_subjects_schema import (
    SessionSubjectCreate, SessionSubjectUpdate)
from src.helpers import ValidationHelper


class SessionSubjectService:
    """Service for managing sessions_subjects"""

    VALID_STATUSES = {"Pending", "Confirmed", "Refused"}

    @staticmethod
    def _validate_status_and_datetimes(data: SessionSubjectCreate | SessionSubjectUpdate):
        """Valide le statut et la cohérence des datetimes."""
        # Validation du statut
        if data.status and data.status not in SessionSubjectService.VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid status '{data.status}'. Allowed values are: "
                    f"{', '.join(SessionSubjectService.VALID_STATUSES)}."
                )
            )

        start_dt = data.start_at
        end_dt = data.end_at

        if start_dt and end_dt and end_dt <= start_dt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_at must be strictly greater than start_at."
            )

    @staticmethod
    async def _load_full_session_subject(session: AsyncSession, session_subject_id: int) -> SessionSubject:
        """Charge complètement un SessionSubject avec toutes les relations nécessaires."""
        query = (
            select(SessionSubject)
            .options(
                selectinload(SessionSubject.classroom_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.class_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.subject_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.user_info),
            )
            .where(SessionSubject.id == session_subject_id)
        )

        result = await session.execute(query)
        session_subject = result.scalar_one_or_none()

        if not session_subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SessionSubject with ID {session_subject_id} not found"
            )
        return session_subject

    @staticmethod
    async def create_session_subject(data: SessionSubjectCreate, session: AsyncSession):
        """Create a new session_subject"""
        try:
            SessionSubjectService._validate_status_and_datetimes(data)

            classroom = None
            if data.classrooms_id:
                classroom = await ValidationHelper.validate_id(Classroom, data.classrooms_id, session, "Classroom")
            assignment = await ValidationHelper.validate_id(AssignmentSubject, data.assignments_subjects_id, session, "AssignmentSubject")

            session_subject = SessionSubject(**data.dict())
            session_subject.classroom_info = classroom
            session_subject.assignment_info = assignment

            session.add(session_subject)
            await session.commit()
            await session.refresh(session_subject)
            logger.info(f"SessionSubject created successfully with ID: {session_subject.id}")

            return await SessionSubjectService._load_full_session_subject(session, session_subject.id)

        except HTTPException as e:
            logger.error(f"HTTP Exception during creation: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error creating SessionSubject: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create session_subject"
            )

    @staticmethod
    async def get_session_subject_by_id(session_subject_id: int, session: AsyncSession):
        """Fetch a session_subject by ID with related entities"""
        try:
            session_subject = await SessionSubjectService._load_full_session_subject(session, session_subject_id)
            logger.info(f"Fetched SessionSubject with ID: {session_subject_id}")
            return session_subject
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error fetching SessionSubject with ID {session_subject_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch session_subject")

    @staticmethod
    async def list_session_subjects(session: AsyncSession):
        """List all session_subjects"""
        try:
            query = (
                select(SessionSubject)
                .options(
                    selectinload(SessionSubject.classroom_info),
                    selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.class_info),
                    selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.subject_info),
                    selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.user_info),
                )
            )
            result = await session.execute(query)
            sessions = result.scalars().all()
            logger.info(f"Fetched {len(sessions)} SessionSubjects")
            return sessions
        except Exception as e:
            logger.error(f"Error listing SessionSubjects: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to list session_subjects"
            )

    @staticmethod
    async def update_session_subject(session_subject_id: int, data: SessionSubjectUpdate, session: AsyncSession):
        """Update an existing session_subject"""
        try:
            session_subject = await SessionSubjectService.get_session_subject_by_id(session_subject_id, session)

            SessionSubjectService._validate_status_and_datetimes(data)

            if data.classrooms_id is not None:
                await ValidationHelper.validate_id(Classroom, data.classrooms_id, session, "Classroom")

            if data.assignments_subjects_id is not None:
                await ValidationHelper.validate_id(AssignmentSubject, data.assignments_subjects_id, session, "AssignmentSubject")

            updated_fields = data.dict(exclude_unset=True)

            for field, value in updated_fields.items():
                setattr(session_subject, field, value)

            await session.commit()
            await session.refresh(session_subject)
            logger.info(f"SessionSubject with ID {session_subject_id} updated successfully")

            return await SessionSubjectService._load_full_session_subject(session, session_subject_id)

        except HTTPException as e:
            logger.error(f"HTTP Exception during update: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error updating SessionSubject: {str(e)}")
            if "ForeignKeyViolationError" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid foreign key value provided. Please ensure that related records exist before updating."
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update session_subject"
            )

    @staticmethod
    async def delete_session_subject(session_subject_id: int, session: AsyncSession):
        """Delete a session_subject"""
        try:
            session_subject = await SessionSubjectService.get_session_subject_by_id(session_subject_id, session)
            await session.delete(session_subject)
            await session.commit()
            logger.info(f"SessionSubject with ID {session_subject_id} deleted successfully")
            return {"detail": "SessionSubject deleted successfully"}
        except HTTPException as e:
            logger.error(f"HTTP Exception during deletion: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error deleting SessionSubject: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete session_subject"
            )
