from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import BaseResponseSchema
from app.infra.database.adapter import get_session_adapter

from .domain import CreateMeetingsUseCase, GetMeetingsUseCase
from .schemas import Meeting

router = APIRouter()


@router.get("/")
async def get_meetings(
    database_session: AsyncSession = Depends(get_session_adapter),
):
    use_case = GetMeetingsUseCase(database_session)
    return await use_case.execute()


@router.post("/")
async def create_meeting(meeting: Meeting) -> BaseResponseSchema:
    return await CreateMeetingsUseCase([meeting]).execute()
