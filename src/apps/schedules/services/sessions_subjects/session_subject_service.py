from datetime import datetime, timedelta

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.apps.schedules.model.classes.classes_model import Classes
from src.apps.classrooms.model.classroom_model import Classroom
from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import AssignmentSubject
from src.apps.schedules.services.assignments_subjects.assignments_subjects_services import AssignmentsSubjectsService
from src.apps.schedules.model.classes.classes_model import Classes
from src.apps.schedules.services.classes.classes_service import ClassService
from src.apps.schedules.model.sessions_subjects.sessions_subjects_model import SessionSubject
from src.apps.schedules.model.sessions_subjects.sessions_subjects_schema import (
    SessionSubjectCreate, SessionSubjectUpdate)
from src.apps.schedules.model.subjects.subjects_model import Subjects
from src.apps.users.model.user.user_model import User
from src.helpers import ValidationHelper
from src.libraries import Combinator
from src.apps.schedules.services.years_groups_educational_courses.years_groups_educational_courses_service import YearsGroupsEducationalCoursesService
from src.apps.schedules.model.sessions_subjects.sessions_subjects_schema  import SessionStatus

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
            existing_class = await ClassService.get_class_by_id(data.classes_id, session)
            if not existing_class:
                raise ValueError(f"Class with ID {data.classes_id} not found")
            
            as_query = (
                select(AssignmentSubject)
                .options(
                    joinedload(AssignmentSubject.class_info),
                    joinedload(AssignmentSubject.subject_info),
                    joinedload(AssignmentSubject.user_info).selectinload(User.availabilities)
                )
                .where(AssignmentSubject.classes_id == data.classes_id)
            )
            as_result = await session.execute(as_query)
            assignedSubjects = as_result.scalars().all()
            if not assignedSubjects:
                raise ValueError(f"No assigned subjects found for class with ID {data.classes_id}")
            
            assignedSubjects =  SessionSubjectService._cast_to_combinator_struct(assignedSubjects)
            calendar = await YearsGroupsEducationalCoursesService.get_year_group_educational_class_by_year_group(
                existing_class.years_group_id, session
            )
            t_calendar = SessionSubjectService._transform_calendar(calendar)
            session_duration = 240
            days_time_slot = (480, 1200)
            nb_rooms= 5

            combinator = Combinator(t_calendar, assignedSubjects, session_duration, days_time_slot, nb_rooms)
            planned_sessions = combinator.solve()
            if planned_sessions.get("status") == "INFEASIBLE":
                raise HTTPException(status_code=400, detail="No feasible schedule found")
            
            session_subjects = []
            for session_data in planned_sessions.get("sessions"):
                start_at = SessionSubjectService.generate_timestamp(session_data['day'], session_data['start_time'])
                end_at = SessionSubjectService.generate_timestamp(session_data['day'], session_data['end_time'])
                session_subject = SessionSubject(
                    assignments_subjects_id=session_data['course_id'],
                    start_at=start_at,
                    end_at=end_at,
                    status=SessionStatus.pending,
                )
                session.add(session_subject)
                await session.commit()
                session_subjects.append(session_subject)
                
            return session_subjects
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
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
    
    @staticmethod
    async def get_teacher_sessions(teacher_id: int, session: AsyncSession):
        teacher_user = await ValidationHelper.validate_id(User, teacher_id, session, "User")

        query = (
            select(SessionSubject)
            .options(
                selectinload(SessionSubject.classroom_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.class_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.subject_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.user_info),
            )
            .join(SessionSubject.assignment_info)
            .where(AssignmentSubject.users_id == teacher_id)
        )

        result = await session.execute(query)
        sessions = result.scalars().all()
        logger.info(f"Fetched {len(sessions)} SessionSubjects for teacher ID: {teacher_id}")
        return sessions

    @staticmethod
    async def get_class_sessions(class_id: int, session: AsyncSession):
        await ValidationHelper.validate_id(Classes, class_id, session, "Classes")

        query = (
            select(SessionSubject)
            .options(
                selectinload(SessionSubject.classroom_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.class_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.subject_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.user_info),
            )
            .join(SessionSubject.assignment_info)
            .where(AssignmentSubject.classes_id == class_id)
        )

        result = await session.execute(query)
        sessions = result.scalars().all()
        logger.info(f"Fetched {len(sessions)} SessionSubjects for class ID: {class_id}")
        return sessions

    @staticmethod
    async def get_subject_sessions(subject_id: int, session: AsyncSession):
        await ValidationHelper.validate_id(Subjects, subject_id, session, "Subject")

        query = (
            select(SessionSubject)
            .options(
                selectinload(SessionSubject.classroom_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.class_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.subject_info),
                selectinload(SessionSubject.assignment_info).selectinload(AssignmentSubject.user_info),
            )
            .join(SessionSubject.assignment_info)
            .where(AssignmentSubject.subjects_id == subject_id)
        )

        result = await session.execute(query)
        sessions = result.scalars().all()
        logger.info(f"Fetched {len(sessions)} SessionSubjects for subject ID: {subject_id}")
        return sessions
    
    @staticmethod
    def _parse_availability(availabilities):
        availability = {}
        for availability_item in availabilities:
            slots = availability_item.slots
            for slot in slots:
                start = datetime.fromisoformat(slot["start_at"])
                end = datetime.fromisoformat(slot["end_at"])
                date_key = start.strftime("%Y-%m-%d")
                start_minutes = start.hour * 60 + start.minute
                end_minutes = end.hour * 60 + end.minute
                
                if date_key not in availability:
                    availability[date_key] = []
                availability[date_key].append((start_minutes, end_minutes))
        
        return availability
    

    @staticmethod
    def _cast_to_combinator_struct(data):
        courses = []
        for item in data:
            course = {
                "id": item.id,
                "name": item.subject_info.name,
                "hourly_volume": item.subject_info.hourly_volume,
                "start_date": item.subject_info.start_at,
                "end_date": item.subject_info.end_at,
                "teacher": {
                    "id": item.user_info.id,
                    "name": f"{item.user_info.first_name} {item.user_info.last_name}",
                    "availability": SessionSubjectService._parse_availability(item.user_info.availabilities)
                    if item.user_info.availabilities else {}
                },
            }
            courses.append(course)
        return courses
    
    def _transform_calendar(calendar):
        transformed_calendar = []
        
        for i, item in enumerate(calendar):
            transformed_calendar.append({
                "id": item.educational_courses_id,
                "date": item.educational_course.day,
                "type": item.day_type
            })
        
        return transformed_calendar
    
    @staticmethod
    def generate_timestamp(day: str, start_time: int) -> datetime:
        day_datetime = datetime.strptime(day, "%Y-%m-%d")
        timestamp = day_datetime + timedelta(minutes=start_time)
        
        return timestamp