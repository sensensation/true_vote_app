from dependency_injector import containers, providers

from app.app_layer.services.vote.service import VoteService
from app.config import settings
from app.infra.db.connection import AlchemyDatabase
from app.infra.http.initilizer import init_coindesk_client
from app.infra.unit_of_work.uow import Uow


class Container(containers.DeclarativeContainer):
    # infra : db + uow
    db = providers.Singleton(AlchemyDatabase, settings=settings.DB)
    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)

    # infra: transports
    coindesk_client = providers.Resource(
        init_coindesk_client,
        base_url=settings.COINDESK.BASE_URL,
        timeout=settings.COINDESK.HTTP_TIMEOUT,
    )

    # app_layer: services
    vote_service = providers.Factory(
        VoteService,
        uow=uow,
    )
