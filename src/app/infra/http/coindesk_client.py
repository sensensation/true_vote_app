import aiohttp
from typing import Optional
from aiohttp import ClientSession, ClientTimeout


class CoindeskClient:
    def __init__(self, base_url: str, http_timeout: int = 10):
        self._base_url = base_url
        self._http_timeout = http_timeout
        self._session: Optional[ClientSession] = None

    async def startup(self) -> None:
        """Создаём aiohttp-сессию с заданным таймаутом."""
        if not self._session:
            self._session = aiohttp.ClientSession(timeout=ClientTimeout(total=self._http_timeout))

    async def shutdown(self) -> None:
        """Закрываем сессию."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def get_btc_price(self) -> float:
        """
        Запрашиваем текущий курс BTC (в долларах) у Coindesk.
        """
        if not self._session:
            await self.startup()

        async with self._session.get(self._base_url) as response:
            data = await response.json()
            # Пример структуры ответа:
            # {
            #   "time": {...},
            #   "bpi": {
            #       "USD": {"rate_float": 27600.50, ...},
            #       ...
            #   },
            #   ...
            # }
            return float(data["bpi"]["USD"]["rate_float"])
