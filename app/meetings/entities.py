from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Entity, TimestampMixin


class MeetingEntity(Entity, TimestampMixin):
    title: Mapped[str]
    start_time: Mapped[datetime] = mapped_column(sqlalchemy.DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(sqlalchemy.DateTime(timezone=True))
    location: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=True)
    attendees: Mapped[str] = mapped_column(sqlalchemy.Text, nullable=True)
