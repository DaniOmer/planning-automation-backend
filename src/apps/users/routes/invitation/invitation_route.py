from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.apps.users import *
from src.config.database_service import get_db
from src.helpers import TransformHelper
from src.apps.users import InvitationCreateSchema

router = APIRouter(prefix="/users/invitation")

@router.post("/send", response_class=JSONResponse)
async def send_registration_invitation(
    data: InvitationCreateSchema, 
    current_user: dict = Depends(SecurityHelper.get_current_user),
    session: AsyncSession = Depends(get_db)
):
    try:
        invitation = await InvitationService.create_invitation(current_user, data, session)
        invitation_dict = TransformHelper.map_to_dict(invitation)
        return InvitationReadSchema(**invitation_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/accept/{token}", response_class=JSONResponse)
async def accept_registration_invitation(
    token: str, 
    session: AsyncSession = Depends(get_db)
):
    try:
        invitation = await InvitationService.accept_invitation(token, session)
        invitation_dict = TransformHelper.map_to_dict(invitation)
        return InvitationReadSchema(**invitation_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))