from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.apps.users import UserCreate, UserService
from src.config.database_service import get_db

router = APIRouter(prefix="/users")

@router.post("/users/", response_class=JSONResponse)
async def create_user(
    user_data: UserCreate, 
    session: AsyncSession = Depends(get_db)
):
    try:
        user_dict = user_data.model_dump() 
        user = await UserService.create_user(user_dict, session)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
