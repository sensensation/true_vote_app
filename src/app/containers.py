from app.config import settings
from app.infra.db.connection import AlchemyDatabase
from dependency_injector import containers, providers

from app.infra.unit_of_work.uow import Uow


class Container(containers.DeclarativeContainer):
    # infra : db + uow
    db = providers.Singleton(AlchemyDatabase, settings=settings.DB)
    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)
