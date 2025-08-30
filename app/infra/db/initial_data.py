from typing import Any

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Table


def insert_initial_electoral_states(_target: Table | None, connection: Connection, **_kwargs: Any) -> None:
    session_maker = sessionmaker(bind=connection)
    session = session_maker()

    # TODO: Добавить начальные данные для миграции
    # session.add(
    #     ElectoralsOrm(
    #         name=...,
    #         value=...,
    #     )
    # )

    session.commit()
