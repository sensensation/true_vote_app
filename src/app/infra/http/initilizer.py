from typing import Any, AsyncGenerator

from app.infra.http.coindesk_client import CoindeskClient


async def init_coindesk_client(
    base_url: str,
    timeout: int,
    **kwargs: Any,
) -> AsyncGenerator[CoindeskClient, None]:
    client = CoindeskClient(
        base_url=base_url,
        **kwargs,
    )
    yield client
    await client.shutdown()
