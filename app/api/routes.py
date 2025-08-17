from fastapi import APIRouter

from app.meetings.routes import router as meetings_router

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


router.include_router(meetings_router, prefix="/meetings", tags=["Meetings"])
