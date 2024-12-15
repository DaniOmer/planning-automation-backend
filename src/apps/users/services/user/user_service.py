from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.apps.schedules.model.assignments_subjects.assignments_subjects_model import \
    AssignmentSubject
from src.apps.users import *
from src.apps.users import User
from src.helpers import SecurityHelper


class UserService:
    """Service for operations related to users"""

    @staticmethod
    async def create_user(session: AsyncSession, user_data, user_role, token=None):
        try:
            created_by = None
            if token is not None:
                query = select(Invitation).where(Invitation.token == token)
                result = await session.execute(query)
                invitation = result.scalar_one_or_none()
                if not invitation:
                    raise ValueError("Invalid invitation token.")
                created_by = invitation.id

            hashed_password = SecurityHelper.get_password_hash(user_data.password)
            user = User(
                email=user_data.email,
                password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                role=user_role,
                phone_number=user_data.phone_number,
                created_by=created_by,
            )
            session.add(user)
            await session.commit()

            logger.info(f"User created successfully with email: {user.email}")
            return user
        except IntegrityError as e:
            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists. Please use another email."
                )
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    @staticmethod
    async def authenticate_user(session: AsyncSession, user_data):
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
    
    @staticmethod
    async def get_all_teachers(session: AsyncSession):
        """Récupère tous les utilisateurs ayant le rôle teacher."""
        query = select(User).where(User.role == RoleEnum.teacher)
        result = await session.execute(query)
        teachers = result.scalars().all()
        return teachers
    
    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with ID {user_id} not found."
            )
        return user

            
    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession):
        """Supprime un utilisateur après avoir vérifié qu'il n'est pas assigné."""
        user = await UserService.get_user_by_id(user_id, session)
        try:
            if user.role == RoleEnum.teacher:
                query = select(AssignmentSubject).where(AssignmentSubject.users_id == user_id)
                result = await session.execute(query)
                assignments = result.scalars().all()

                if assignments:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Cannot delete teacher with ID {user_id} because they are assigned to a subject."
                    )
            
            await session.delete(user)
            await session.commit()
            logger.info(f"User with ID {user_id} successfully deleted.")
        except HTTPException as e:
            logger.error(f"HTTP Exception during deletion: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error deleting user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user."
            )



