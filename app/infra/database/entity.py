from datetime import UTC, datetime
from typing import Any, ClassVar, NewType, final, override

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from typeid import TypeID

from .adapter import metadata

Text = NewType("Text", str)


@final
class GUID(sa.types.TypeDecorator[TypeID]):
    """Custom GUID type for SQLAlchemy."""

    impl = sa.String(36)
    cache_ok = True

    @override
    def process_bind_param(
        self, value: TypeID | str | None, dialect: sa.engine.Dialect
    ) -> str | None:
        if value is None:
            return None
        return str(value)

    @override
    def process_result_value(
        self, value: str | None, dialect: sa.engine.Dialect
    ) -> TypeID | None:
        if value is None:
            return None
        return TypeID.from_string(value)


class Entity(DeclarativeBase):
    """Base class for all ORM entities, using shared metadata."""

    type_annotation_map: ClassVar[dict[Any, Any]] = {
        str: sa.String(255),
        Text: sa.Text(),
        datetime: sa.TIMESTAMP(timezone=True),
        TypeID: GUID(),
    }

    metadata: ClassVar[sa.MetaData] = metadata

    @declared_attr.directive
    def __tablename__(cls):
        # Automatically generate __tablename__ from class name
        return cls.__name__.lower().removesuffix("entity")

    id_: Mapped[TypeID] = mapped_column("id", primary_key=True, nullable=False)


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
