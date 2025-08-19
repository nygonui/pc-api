from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text

from app.api.schemas import BaseResponseSchema

from .schemas import Meeting


@dataclass
class GetMeetingsUseCase:
    database_session: AsyncSession

    async def execute(self) -> BaseResponseSchema:
        result = await self.database_session.execute(
            text("select 'hello world'")
        )
        return BaseResponseSchema(
            status=200,
            message="Meetings fetched successfully",
            data=result.scalars().all(),
        )


@dataclass
class CreateMeetingsUseCase:
    meeting: list[Meeting]

    async def execute(self) -> BaseResponseSchema:
        return BaseResponseSchema(
            status=200,
            message="Meetings created successfully",
            data=self.meeting,
        )
