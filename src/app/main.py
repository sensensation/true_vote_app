from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

from fastapi import FastAPI

from app.api import rest
from app.api.rest.controllers import init_rest_api
from app.config import settings
from app.containers import Container

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    app_.state.container = Container()
    app_.state.container.wire(
        packages=[
            rest,
            # Импортировать сюда дополнительные контроллеры
        ]
    )
    logger.info("Container resources: %s", app_.state.container.providers)

    await app_.state.container.init_resources()  # type: ignore[misc]

    # Если нужно прикрутить клиент к приложению .state:
    # app_.state.some_web_client = get_some_web_client()

    yield

    # await app_.state.some_web_client.shutdown()

    await app_.state.container.shutdown_resources()  # type: ignore[misc]


def init_api_docs(app: FastAPI, *, show_docs: bool, api_root: str) -> None:
    if not show_docs:
        return

    app.docs_url = "/docs"
    app.redoc_url = "/redoc"
    app.openapi_url = "/openapi.json"
    app.setup()


app = FastAPI(version=settings.API.DOCS_VERSION, lifespan=lifespan)

init_api_docs(app, show_docs=settings.API.DOCS_ENABLED, api_root=settings.API.PUBLIC_PREFIX)
init_rest_api(app)
