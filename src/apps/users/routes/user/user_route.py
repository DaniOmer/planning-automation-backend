from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.apps.users import *
from src.config.database_service import get_db
from src.helpers import TransformHelper
from src.helpers import SecurityHelper

router = APIRouter(prefix="/users")

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
        data = await UserService.authenticate_user(user_data, session)
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