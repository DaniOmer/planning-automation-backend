from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import openai
import os
from dotenv import load_dotenv
from src.config.database_service import get_db
from src.apps.schedules.services.ai.ai_services import find_teachers_for_subject

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupérer la clé API OpenAI depuis .env
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("La clé API OpenAI n'est pas configurée. Vérifiez votre fichier .env.")

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/available_teachers")
async def available_teachers_route(
    subject_id: int,
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession = Depends(get_db),
):
    """
    Endpoint pour récupérer les enseignants disponibles pour un sujet donné dans une plage horaire.
    """
    # Étape 1 : Récupérer les enseignants disponibles via le service
    teachers = await find_teachers_for_subject(subject_id, start_date, end_date, session)

    if not teachers:
        raise HTTPException(status_code=404, detail="Aucun enseignant disponible trouvé pour cette plage horaire.")

    # Étape 2 : Formater les données pour l'IA
    formatted_teachers = [
        f"{teacher['name']} ({teacher['email']})"
        for teacher in teachers
    ]
    teachers_text = "\n".join(formatted_teachers)

    # Vérification si des enseignants sont trouvés avant d'appeler OpenAI
    if not formatted_teachers:
        return {
            "teachers": teachers,
            "ai_response": "Aucun enseignant disponible n'a été trouvé pour ce sujet et cette plage horaire."
        }

    # Étape 3 : Générer une réponse avec OpenAI
    try:
        ai_response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Vous êtes un assistant qui aide à trouver des enseignants disponibles pour enseigner un sujet spécifique."
                },
                {
                    "role": "user",
                    "content": (
                        f"Voici une liste des enseignants disponibles pour enseigner le sujet avec l'ID {subject_id} "
                        f"entre {start_date} et {end_date} :\n{teachers_text}\n"
                        "Pouvez-vous indiquer les enseignants les plus adaptés à enseigner ce sujet ?"
                    )
                },
            ],
        )
        return {
            "teachers": teachers,
            "ai_response": ai_response.choices[0].message["content"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la communication avec OpenAI : {str(e)}")
