from src.apps.users import User
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from loguru import logger

from src.apps.users import User

class UserService:
    """Service for operations related to users"""

    @staticmethod
    async def create_user(user_data: User, session: AsyncSession):
        try:
            user = User(**user_data)
            session.add(user)
            await session.commit()

            logger.info(f"User created successfully with email: {user.email}")
            return user
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        