from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from loguru import logger

from src.apps.users import Invitation, InvitationCreateSchema
from src.helpers import SecurityHelper, MessengerHelper, EmailData
from config import *

class InvitationService:
    """Service for operations related to user invitations."""

    @staticmethod
    async def create_invitation(inviter, data: InvitationCreateSchema, session: AsyncSession):
        try:
            stmt = await session.execute(select(Invitation).where(Invitation.email == data.email))
            existing_invitation = stmt.scalar_one_or_none()
            if existing_invitation:
                raise ValueError("An invitation already exists for the given email.")

            invited_by = int(inviter['sub'])
            token=SecurityHelper.generate_random_token()
            expires_at = datetime.now()
            expires_at += timedelta(days=int(INVITATION_EXPIRATION_DAYS))
            invitation = Invitation(
                first_name=data.first_name, 
                last_name=data.last_name,
                email=data.email, 
                invited_by=invited_by, 
                token=token,
                is_disabled=False,
                expires_at=expires_at
            )
            session.add(invitation)
            await session.commit()

            InvitationService.send_invitation_email(invitation)
            logger.info(f"Invitation succefully sent to teacher with email: {invitation.email}")
            
            return invitation
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod
    def send_invitation_email(invitation):
        email_data = EmailData(
            to_email=invitation.email,
            subject=f"Invitation to join {invitation.first_name} {invitation.last_name}'s class",
            html_content=f"""
                <h1>Invitation to join Planify</h1>
                <p>Click the link below to accept the invitation:</p>
                <a href="{FRONTEND_URL}/users/invitation/accept/{invitation.token}">Accept Invitation</a>
                <p>Copie the following link if the invitation button does not working : {FRONTEND_URL}/users/invitation/accept/{invitation.token}</p>
                <p>This invitation will expire in {INVITATION_EXPIRATION_DAYS} days.</p>
            """,
            text_content=f"Invitation to join Planify. Click the link below to accept the invitation: {FRONTEND_URL}/users/invitation/accept/{invitation.token}"
        )
        MessengerHelper.send_email(email_data)