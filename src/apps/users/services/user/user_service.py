from src.apps.users import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from loguru import logger

from src.apps.users import User, UserCreate, UserLogin
from src.helpers import SecurityHelper

class UserService:
    """Service for operations related to users"""

    @staticmethod
    async def create_user(user_data: UserCreate, session: AsyncSession):
        try:
            hashed_password = SecurityHelper.get_password_hash(user_data.password)
            user = User(
                email=user_data.email, 
                password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                role=user_data.role,
                phone_number=user_data.phone_number,
            )
            session.add(user)
            await session.commit()

            logger.info(f"User created successfully with email: {user.email}")
            return user
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    @staticmethod
    async def authenticate_user(user_data: UserLogin, session: AsyncSession):
        query = select(User).where(User.email == user_data.email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user and SecurityHelper.verify_password(user_data.password, user.password):
            logger.info(f"User authenticated successfully with email: {user.email}")
            token = SecurityHelper.create_access_token({
                "sub": str(user.id),
                "email": user.email, 
                "role": user.role
            })
            return [user, token]
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        