from abc import ABC, abstractmethod

from app.app_layer.interfaces.kafka.schemas import VotesKafkaRequest


class AbstractKafkaProducer(ABC):
    @abstractmethod
    async def send_vote_request(self, message: VotesKafkaRequest) -> None:
        """Send vote message into kafka"""
