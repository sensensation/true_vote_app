from dependency_injector import containers, providers

from app.app_layer.services.votes.create_vote.service import VoteCreateService
from app.app_layer.services.votes.get_vote.serivce import VoteGetService
from app.config import settings
from app.infra.db.connection import AlchemyDatabase
from app.infra.unit_of_work.uow import Uow


class Container(containers.DeclarativeContainer):
    # infra : db + uow
    db = providers.Singleton(AlchemyDatabase, settings=settings.DB)
    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)

    # infra: transports
    # coindesk_client = providers.Resource(
    #     # any http client
    #     base_url=settings.COINDESK.BASE_URL,
    #     timeout=settings.COINDESK.HTTP_TIMEOUT,
    # )

    # app_layer: services
    vote_get_service = providers.Factory(
        VoteGetService,
        uow=uow,
    )
    vote_create_service = providers.Factory(
        VoteCreateService,
        uow=uow,
    )
    # room_create_service = providers.Factory(
    #     RoomCreateService,
    #     uow=uow,
    # )
