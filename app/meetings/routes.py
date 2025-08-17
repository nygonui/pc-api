from fastapi import APIRouter

from app.api.schemas import BaseResponseSchema

from .domain import CreateMeetingsUseCase
from .schemas import Meeting

router = APIRouter()


@router.get("/")
async def get_meetings():
    return []


@router.post("/")
async def create_meeting(meeting: Meeting) -> BaseResponseSchema:
    return CreateMeetingsUseCase([meeting]).execute()
