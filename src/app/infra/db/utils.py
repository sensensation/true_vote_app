from typing import Any, Callable

import orjson
from pydantic import BaseModel
from pydantic_core import to_jsonable_python


def orjson_dumper(value: Any, *, default: Callable[[Any], Any] = to_jsonable_python) -> str:
    return orjson.dumps(value, default=default).decode()


def model_dump(
    model: BaseModel,
    *,
    exclude_unset: bool = False,
    exclude_none: bool = False,
    by_alias: bool = True,
) -> dict[str, Any]:
    return model.model_dump(exclude_unset=exclude_unset, exclude_none=exclude_none, by_alias=by_alias)  # type: ignore
