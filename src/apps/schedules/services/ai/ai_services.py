from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import AssignmentSubject
from src.apps.schedules.model.availabilities.availabilities_model import Availabilities
import openai
import json


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

async def generate_availability_json(availability_text: str):
    """
    Génère un JSON structuré des disponibilités à partir d'un texte donné.

    :param availability_text: Texte décrivant les disponibilités.
    :return: JSON structuré des disponibilités.
    """
    prompt = (
        "Je veux que tu prennes le texte ci-dessous qui décrit les disponibilités d'un enseignant "
        "et que tu génères un JSON structuré. Le JSON doit contenir une liste de dates, et pour chaque date, "
        "indiquer si l'enseignant est disponible le matin ('morning': TRUE/FALSE) et/ou l'après-midi ('afternoon': TRUE/FALSE). "
        "Exemple de JSON attendu :\n"
        "[\n"
        "    {\"date\": \"2024-12-09\", \"morning\": TRUE, \"afternoon\": FALSE},\n"
        "    {\"date\": \"2024-12-10\", \"morning\": TRUE, \"afternoon\": FALSE}\n"
        "]\n"
        f"Voici le texte de l'enseignant : {availability_text}"
        f"Ne reponds rien de plus que le json"
    )

    try:
        ai_response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant qui aide à transformer des disponibilités exprimées en langage naturel en un JSON structuré."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_content = ai_response.choices[0].message["content"]
        print("Réponse brute de l'IA :", response_content)  # Log pour inspection

        try:
            availability_json = json.loads(response_content)
            return availability_json
        except json.JSONDecodeError:
            raise ValueError(f"L'IA a généré une réponse invalide. Réponse brute : {response_content}")

    except openai.error.OpenAIError as e:
        raise ValueError(f"Erreur lors de la communication avec OpenAI : {str(e)}")
