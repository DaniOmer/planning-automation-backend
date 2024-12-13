from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from src.config.database_service import get_db
from src.apps.schedules.services.ai.ai_services import *
from src.helpers.security_helper import SecurityHelper

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
    current_user=Depends(SecurityHelper.get_current_user)
):
    """
    Endpoint pour récupérer les enseignants disponibles pour un sujet donné dans une plage horaire.
    """
    # Récupérer les enseignants et leurs disponibilités
    teachers, availabilities = await get_all_teachers_and_availabilities(subject_id, session)

    if not teachers:
        raise HTTPException(status_code=404, detail="Aucun enseignant trouvé pour ce sujet.")

    # Préparer les données pour l'IA
    all_teachers_text = "\n".join([
        f"{teacher['name']} ({teacher['email']}, {teacher['phone_number']})"
        for teacher in teachers
    ])

    availabilities_text = "\n".join([
        f"User ID {availability['user_id']}: {availability['start_at']} - {availability['end_at']}"
        for availability in availabilities
    ])

    # Générer une réponse avec OpenAI
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
                        f"Je veux que tu m'aides à trouver des professeurs qui enseignent le sujet avec l'ID {subject_id} "
                        f"et qui sont disponibles entre {start_date} et {end_date}. Voici la liste des professeurs de mon école "
                        f"qui enseignent le sujet avec l'ID {subject_id} :\n{all_teachers_text}\n"
                        f"Et voici leurs disponibilités :\n{availabilities_text}\n"
                        "Réponds-moi en me disant que grâce à toutes les données de la base de données voici la liste des professeurs disponibles dans ma tranche horaire transmise sous forme de tirets : "
                        "- Prénom NOM (mail numéro)."
                        f"Si tu ne trouves aucun resultat, reponds qu'aucun professeur n'est disponible pour cette matière entre le {start_date} et {end_date}"
                        f"Réponse professionnelles seulement"
                    )
                },
            ],
        )
        return {
            "ai_response": ai_response.choices[0].message["content"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la communication avec OpenAI : {str(e)}")


class AvailabilityRequest(BaseModel):
    availability_text: str

@router.post("/professor_availability")
async def professor_availability_route(
    availability_data: AvailabilityRequest,
    current_user=Depends(SecurityHelper.get_current_user)
):
    """
    Endpoint pour générer un JSON structuré des disponibilités d'un professeur à partir d'un texte libre.
    """
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux enseignants.")

    try:
        availability_json = await generate_availability_json(availability_data.availability_text)
        return {"availability_json": availability_json}

    except ValueError as e:
        print("Erreur d'analyse :", str(e))  # Log la réponse brute pour inspection
        raise HTTPException(status_code=500, detail=str(e))