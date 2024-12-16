import asyncio
import inspect
import logging
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Coroutine, Optional

import jsonpickle
from cashews import Cache as CashewsCache
from x5d_web.transport.http.v1.keycloak_client import AbstractCache as KeycloakAbstractCache

from app.config import KeycloakCacheSetting, settings
from app.redis import RedisClient, redis

logger = logging.getLogger(__name__)


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass



class RedisCache(AbstractCache):
    def __init__(self) -> None:
        self.client: RedisClient = redis

    async def get(self, key: str) -> Optional[str | bytes]:
        try:
            value = await self.client.pool.get(key)
            logger.debug("Get cache with key %s", key)
            return value
        except Exception as e:
            logger.exception(f"Exception on get cache with key {key}: {e}")
            return None

    async def set(self, key: str, value: str | bytes, expire: int) -> None:
        try:
            # do not wait for result
            asyncio.ensure_future(self.client.pool.set(key, value, expire=expire))
            logger.debug("Set cache with key %s", key)
        except Exception as e:
            logger.exception(f"Exception on set cache with key {key}: {e}")

    async def delete(self, key: str) -> None:
        """
        UNLINK performs the actual memory reclaiming in a different thread,
        so it is not blocking, while DEL is.
        """
        try:
            keys = await self.client.pool.keys(f"{key}*")

            if not keys:
                return

            # do not wait for result
            asyncio.ensure_future(self.client.pool.unlink(*keys))

            logger.debug(f"Delete cache with key {key}")
        except Exception as e:
            logger.exception(f"Exception on delete cache with key {key}: {e}")


cache_type_mapper = {
    "RedisCache": RedisCache,
}

cache = cache_type_mapper[settings.CACHE.CLIENT_CLASS]()


def cached(
    ttl: Optional[int] = None,
    toggle: Optional[bool] = None,
    key_builder: Optional[Callable[[Any], Any]] = None,
) -> Callable[[Any], Any]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            if not settings.CACHE.ENABLED:
                return await func(*args, **kwargs)

            if toggle is not None and not toggle:
                return await func(*args, **kwargs)

            if key_builder:
                key = key_builder(func, *args, **kwargs)
            else:
                key = build_cache_key(func, *args, **kwargs)

            value = await cache.get(key)
            if value:
                return jsonpickle.decode(value)

            result = await func(*args, **kwargs)

            serialized_result = jsonpickle.encode(result)
            await cache.set(key, serialized_result, expire=ttl)  # type: ignore[arg-type]

            return result

        return wrapper

    return decorator


def build_cache_key(func: Callable[[Any], Any], *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> str:
    """
    Build cache key looks like this:
      /app/code/app/providers/auth.pyAuthProvider.fetch_phone_from_user_auth('Token',)[('a', 1), ('b', 2)]
    """
    ordered_kwargs = sorted(kwargs.items())
    key = f"{func.__globals__['__file__']}{func.__qualname__}{args}{ordered_kwargs}"

    if not args:
        return key

    method = getattr(args[0], func.__name__, None)

    if method and inspect.ismethod(method):
        return f"{func.__globals__['__file__']}{func.__qualname__}{args[1:]}{ordered_kwargs}"

    return key


def invalidate_cache(key_builder: Callable[[Any], Any], toggle: Optional[bool] = None) -> Callable[[Any], Any]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)

            if not settings.CACHE.ENABLED:
                return result

            if toggle is not None and not toggle:
                return result

            key = key_builder(func, *args, **kwargs)
            await cache.delete(key)

            return result

        return wrapper

    return decorator
