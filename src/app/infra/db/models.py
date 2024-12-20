from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Index, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import JSONB as DEFAULT_JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint
from app.domain.votes.enums import DeviceTypeEnum, VoteStatusEnum
from app.infra.db.mixins import TimeMixin

metadata = MetaData()

JSONB = DEFAULT_JSONB(none_as_null=True)  # type: ignore[no-untyped-call]


class Base(DeclarativeBase):
    metadata = metadata


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device: Mapped[str | None] = mapped_column(String(64), comment="Устройство", index=True)
    user_name: Mapped[str | None] = mapped_column(String(64), comment="Имя", index=True)
    user_last_name: Mapped[str | None] = mapped_column(String(64), comment="Фамилия", index=True)
    phone: Mapped[str | None] = mapped_column(String(21), comment="Номер телефона", index=True, unique=True)
    email: Mapped[str | None] = mapped_column(String(128), comment="Электронная почта")

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("user_name", name="uq_users_username"),
    )


class OptionORM(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        comment="Описание варианта голосования"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        nullable=False, 
        comment="Активен ли вариант голосования"
    )
    meta: Mapped[Any] = mapped_column(
        DEFAULT_JSONB, 
        nullable=True, 
        comment="Дополнительные метаданные о варианте"
    )

    __table_args__ = (
        Index("ix_options_description", "description"),
    )


class VoteORM(Base, TimeMixin):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        comment="ID пользователя, который проголосовал",
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey("options.id"),
        nullable=False,
        comment="ID выбора (варианта), за который проголосовали",
    )
    device_type: Mapped[DeviceTypeEnum] = mapped_column(
        String(20),
        nullable=True,
        comment="Тип устройства, с которого был отправлен голос",
    )
    status: Mapped[VoteStatusEnum] = mapped_column(String(20), nullable=False, comment="Статус голоса")
    meta: Mapped[Any] = mapped_column(JSONB, nullable=True, comment="Дополнительные метаданные о голосе")
    blockchain_txn_id: Mapped[UUID] = mapped_column(nullable=True, comment="ID транзакции в блокчейне")

    __table_args__ = (Index("ix_votes_user_id_option_id", "user_id", "option_id"),)
