from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Meeting(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    attendees: List[str] = []
