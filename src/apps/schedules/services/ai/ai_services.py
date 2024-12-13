from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import AssignmentSubject
from src.apps.schedules.model.availabilities.availabilities_model import Availabilities
from src.apps.users.model.user.user_model import User
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

async def find_teachers_for_subject(
    subject_id: int,
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession
):
    """
    Trouve les enseignants disponibles pour un sujet donné dans une plage horaire définie.

    :param subject_id: Identifiant du sujet enseigné.
    :param start_date: Date et heure de début de la plage horaire.
    :param end_date: Date et heure de fin de la plage horaire.
    :param session: Session de base de données asynchrone.
    :return: Liste des enseignants disponibles avec leurs informations.
    """
    # Étape 1 : Récupérer les enseignants associés au sujet
    subject_stmt = select(AssignmentSubject).options(
        joinedload(AssignmentSubject.user_info),
        joinedload(AssignmentSubject.subject_info)
    ).where(AssignmentSubject.subjects_id == subject_id)
    subject_results = await session.execute(subject_stmt)
    assignments = subject_results.scalars().all()

    # Étape 2 : Filtrer les enseignants disponibles
    available_teachers = []
    seen_teachers = set()  # Pour éviter les doublons

    for assignment in assignments:
        teacher = assignment.user_info
        if teacher.role != "teacher":
            continue  # Ignorer si ce n'est pas un enseignant

        # Vérifier les disponibilités de l'enseignant
        availability_stmt = select(Availabilities).where(
            and_(
                Availabilities.users_id == teacher.id,
                Availabilities.start_at <= start_date,
                Availabilities.end_at >= end_date
            )
        )
        availability_result = await session.execute(availability_stmt)
        availability = availability_result.scalar_one_or_none()

        if availability and teacher.id not in seen_teachers:
            available_teachers.append({
                "name": f"{teacher.first_name} {teacher.last_name}",
                "email": teacher.email
            })
            seen_teachers.add(teacher.id)

    return available_teachers
