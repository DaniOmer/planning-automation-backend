from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.apps.users import UserCreate, UserResponse, UserService
from src.config.database_service import get_db
from src.helpers import TransformHelper

router = APIRouter(prefix="/users")

@router.post("/users/", response_class=JSONResponse)
async def create_user(
    user_data: UserCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        user = await UserService.create_user(user_data, session)
        user_dict = TransformHelper.map_to_dict(user)
        return UserResponse(**user_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
