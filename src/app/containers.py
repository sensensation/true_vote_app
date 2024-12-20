from app.config import settings
from app.infra.db.connection import AlchemyDatabase
from dependency_injector import containers, providers

from app.infra.unit_of_work.uow import Uow
from app.app_layer.services.votes.retrieve import RetrieveVoteService
from infra.kafka.producer import KafkaProducer


class Container(containers.DeclarativeContainer):
    # infra : db + uow
    db = providers.Singleton(AlchemyDatabase, settings=settings.DB)
    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)

    # infra: transports
    kafka_producer = providers.Resource(KafkaProducer, settings=settings.KAFKA)

    # app_layer: services
    retrieve_vote_service = providers.Factory(
        RetrieveVoteService,
        uow=uow,
    )
