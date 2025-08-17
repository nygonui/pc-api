from dataclasses import dataclass
from typing import List

from app.api.schemas import BaseResponseSchema

from .schemas import Meeting


@dataclass
class CreateMeetingsUseCase:
    meeting: List[Meeting]

    def execute(self) -> BaseResponseSchema:
        return BaseResponseSchema(
            status=200, message="Meetings created successfully", data=self.meeting
        )
