from typing import Generic, TypeVar

from pydantic import BaseModel as _PydanticBaseModel

BM = TypeVar("BM", bound=_PydanticBaseModel)

T = TypeVar("T", bound=_PydanticBaseModel)


class AggregatePag(_PydanticBaseModel, Generic[T]):
    total: int
    data: list[T]
