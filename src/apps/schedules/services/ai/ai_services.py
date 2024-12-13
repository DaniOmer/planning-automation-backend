from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import AssignmentSubject
from src.apps.schedules.model.availabilities.availabilities_model import Availabilities
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

async def get_all_teachers_and_availabilities(
    subject_id: int,
    session: AsyncSession
):
    """
    Récupère tous les enseignants associés à un sujet avec leurs disponibilités.

    :param subject_id: Identifiant du sujet enseigné.
    :param session: Session de base de données asynchrone.
    :return: Liste des enseignants et leurs disponibilités.
    """
    # Récupérer les enseignants associés au sujet
    teachers_stmt = select(AssignmentSubject).options(
        joinedload(AssignmentSubject.user_info)
    ).where(AssignmentSubject.subjects_id == subject_id)
    teachers_results = await session.execute(teachers_stmt)
    assignments = teachers_results.scalars().all()

    # Construire les données des enseignants et leurs disponibilités
    teachers = []
    availabilities_stmt = select(Availabilities)
    availabilities_results = await session.execute(availabilities_stmt)
    all_availabilities = availabilities_results.scalars().all()

    for assignment in assignments:
        teacher = assignment.user_info
        teachers.append({
            "id": teacher.id,
            "name": f"{teacher.first_name} {teacher.last_name}",
            "email": teacher.email,
            "phone_number": teacher.phone_number
        })

    availabilities = [
        {
            "user_id": availability.users_id,
            "start_at": availability.start_at,
            "end_at": availability.end_at,
        }
        for availability in all_availabilities
    ]

    return teachers, availabilities
