import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database.entity import Entity, TimestampMixin


class CarsEntity(Entity, TimestampMixin):
    brand: Mapped[str] = mapped_column(sa.Text, nullable=False)
    model: Mapped[str] = mapped_column(sa.Text, nullable=False)
    year: Mapped[int] = mapped_column(sa.SmallInteger, nullable=False)
