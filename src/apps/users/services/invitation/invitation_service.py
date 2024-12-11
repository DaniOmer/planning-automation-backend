from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from loguru import logger

from src.apps.users import Invitation, InvitationCreateSchema
from src.helpers import SecurityHelper
from config import *

class InvitationService:
    """Service for operations related to user invitations."""

    @staticmethod
    async def create_invitation(data: InvitationCreateSchema, session: AsyncSession):
        try:
            stmt = await session.execute(select(Invitation).where(Invitation.email == data.email))
            existing_invitation = stmt.scalar_one_or_none()
            if existing_invitation:
                raise ValueError("An invitation already exists for the given email.")

            token=SecurityHelper.generate_token()
            expires_at = datetime.now()
            expires_at += timedelta(days=INVITATION_EXPIRATION_DAYS)
            invitation = Invitation(
                email=data.email, 
                invited_by=data.invited_by, 
                token=token,
                is_disabled=False,
                expires_at=expires_at
            )
            session.add(invitation)
            await session.commit()

            logger.info(f"Invitation succefully sent to teacher with email: {invitation.email}")
            return invitation
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        