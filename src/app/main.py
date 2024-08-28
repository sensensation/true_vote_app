from contextlib import asynccontextmanager
from typing import AsyncIterator
from app.containers import Container
from app.api import rest
from fastapi import FastAPI
from app.config import settings


def init_api_docs(app: FastAPI, *, show_docs: bool, api_root: str) -> None:
    if not show_docs:
        return

    app.docs_url = f"{api_root}/internal/docs"
    app.redoc_url = f"{api_root}/internal/redoc"
    app.openapi_url = f"{api_root}/internal/openapi.json"
    app.setup()


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    app_.state.container = Container()
    app_.state.container.wire(
        packages=[
            rest,
            # Импортировать сюда дополнительные контроллеры
        ]
    )
    await app_.state.container.init_resources()  # type: ignore[misc]

    # Если нужно прикрутить клиент к приложению .state:
    # app_.state.some_web_client = get_some_web_client()

    yield

    # await app_.state.some_web_client.shutdown()

    await app_.state.container.shutdown_resources()  # type: ignore[misc]


app = FastAPI(version=settings.API.DOCS_VERSION, lifespan=lifespan)

init_api_docs(app, show_docs=settings.API.DOCS_ENABLED, api_root=settings.API.PUBLIC_PREFIX)
