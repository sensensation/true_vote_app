from logging import getLogger

from pydantic import BaseModel
from app.config import KafkaSettings, settings
from app_layer.interfaces.kafka.exceptions import KafkaConnectionException, KafkaException, KafkaProducerError, KafkaTopicException
from app_layer.interfaces.kafka.producer import AbstractKafkaProducer
from app_layer.interfaces.kafka.schemas import VotesKafkaRequest
from infra.db.utils import model_dump

logger = getLogger(__name__)


import asyncio
import json
from logging import getLogger

import faust
from aiokafka.errors import KafkaConnectionError, KafkaError
from pydantic import BaseModel

MsgType = BaseModel

logger = getLogger(__name__)


class Producer:
    def __init__(
        self,
        settings: KafkaSettings,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._settings = settings
        self._app = faust.App(
            settings.NAME,
            broker=settings.BROKER,
            autodiscover=True,
            loop=loop,
            debug=settings.DEBUG,
            producer_only=settings.PRODUCER_ONLY,
            producer_request_timeout=settings.PRODUCER_REQUEST_TIMEOUT,
            producer_linger=settings.PRODUCER_LINGER,
        )

    async def startup(self) -> None:
        if not self._settings.ENABLED:
            return
        await self._app.start_client()

    async def shutdown(self) -> None:
        if not self._settings.ENABLED:
            return
        await self._app.stop()

    async def send_message(
        self,
        msg: MsgType,
        key: str | None = None,
        by_alias: bool = True,
        topic: str | None = None,
    ) -> None:
        if not self._settings.ENABLED:
            return

        topic = self._settings.TOPIC if topic is None else topic

        if topic is None:
            raise KafkaTopicException

        try:
            if self._app.should_stop:
                await self._app.restart()

            await self._app.maybe_start_client()
            await self._app.send(
                topic,
                key=key,
                value=model_dump(msg, exclude_unset=True, by_alias=by_alias),
            )
        except KafkaConnectionError as err:
            await self._app.stop()
            raise KafkaConnectionException from err
        except KafkaError as err:
            raise KafkaException from err

    async def send_and_wait_message(
        self,
        msg: MsgType,
        key: str | None = None,
        by_alias: bool = True,
        topic: str | None = None,
    ) -> None:
        if not self._settings.ENABLED:
            return

        topic = self._settings.TOPIC if topic is None else topic

        if topic is None:
            raise KafkaTopicException

        try:
            if self._app.should_stop:
                await self._app.restart()

            await self._app.maybe_start_client()
            await self._app.producer.send_and_wait(
                topic=topic,
                key=bytes(key, "UTF-8") if key else None,
                value=json.dumps(model_dump(msg, exclude_unset=True, by_alias=by_alias)).encode("UTF-8"),
                partition=None,
                timestamp=None,
                headers={},
            )
        except KafkaConnectionError as err:
            await self._app.stop()
            raise KafkaConnectionException from err
        except KafkaError as err:
            raise KafkaException from err




class KafkaProducer(Producer, AbstractKafkaProducer):
    async def send_vote_request(self, message: VotesKafkaRequest) -> None:
        topic = settings.KAFKA.votes_saver.topic
        await self._send_message(message, topic)

    async def _send_message(self, message: BaseModel, topic: str) -> None:
        try:
            return await self.send_message(msg=message, topic=topic)
        except KafkaException:
            logger.exception("Could not send message to kafka")
            raise KafkaProducerError
