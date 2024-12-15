from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users import *
from src.config.database_service import get_db
from src.helpers import SecurityHelper, TransformHelper

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_class=JSONResponse)
async def register(
    user_data: UserCreateSchema, 
    session: AsyncSession = Depends(get_db)
):
    try:
        user_role = RoleEnum.admin
        user = await UserService.create_user(session, user_data, user_role)
        user_dict = TransformHelper.map_to_dict(user)
        return UserResponse(**user_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/register-by-invitation", response_class=JSONResponse)
async def register(
    user_data: UserCreateByInvitationSchema,
    session: AsyncSession = Depends(get_db)
):
    try:
        user_role= RoleEnum.teacher
        user = await UserService.create_user(session, user_data.user, user_role, user_data.token)
        user_dict = TransformHelper.map_to_dict(user)
        return UserResponse(**user_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_class=JSONResponse)
async def login(
    user_data: UserLoginSchema, 
    session: AsyncSession = Depends(get_db)
):
    try:
        data = await UserService.authenticate_user(session, user_data)
        user_dict = TransformHelper.map_to_dict(data[0])
        return LoginResponse(
            user=UserResponse(**user_dict),
            access_token=data[1],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/admin-dashboard")
async def admin_dashboard(current_user=Depends(SecurityHelper.require_role("admin"))):
    return {"message": "Welcome to the admin dashboard", "user": current_user}

@router.get("/teachers", response_class=JSONResponse, response_model=list[UserResponse])
async def get_teachers(
    # current_user: dict = Depends(SecurityHelper.get_current_user),
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.get_current_user)
):
    """Récupère la liste de tous les users avec rôle teacher, accessible uniquement par tous les utilisateurs authentifiés."""
    teachers = await UserService.get_all_teachers(session)
    return [UserResponse(**TransformHelper.map_to_dict(teacher)) for teacher in teachers]

@router.delete("/teachers/{teacher_id}", response_class=JSONResponse)
async def delete_teacher(
    teacher_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(SecurityHelper.require_role("admin")),
):
    """Supprime un teacher, accessible uniquement par l'administrateur."""
    try:
        teacher = await UserService.get_user_by_id(teacher_id, session)
        if teacher.role != RoleEnum.teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="The specified user is not a teacher."
            )
        
        await UserService.delete_user(teacher_id, session)
        return {"detail": f"Teacher with ID {teacher_id} successfully deleted."}
    except HTTPException as e:
        logger.error(f"Error deleting teacher: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting teacher: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to delete teacher."
        )
