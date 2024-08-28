from datetime import datetime

from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from sqlalchemy.sql import func
from typing_extensions import Annotated

timestamp = Annotated[
    datetime,
    mapped_column(nullable=False, default=datetime.utcnow, server_default=func.CURRENT_TIMESTAMP()),
]


@declarative_mixin
class TimeMixin:
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp] = mapped_column(onupdate=datetime.utcnow)


@declarative_mixin
class IndexedTimeMixin(TimeMixin):
    created_at: Mapped[timestamp] = mapped_column(index=True)


@declarative_mixin
class ErrorMixin:
    error_code: Mapped[str | None] = mapped_column(TEXT, comment="Код ошибки")
    error_desc: Mapped[str | None] = mapped_column(TEXT, comment="Текст ошибки")
