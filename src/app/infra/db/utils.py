from typing import Any, Callable
import orjson
from pydantic_core import to_jsonable_python


def orjson_dumper(
    value: Any, *, default: Callable[[Any], Any] = to_jsonable_python
) -> str:
    return orjson.dumps(value, default=default).decode()
