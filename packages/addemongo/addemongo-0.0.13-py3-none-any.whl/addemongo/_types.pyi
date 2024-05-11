from pydantic import BaseModel as _PydanticBaseModel
from typing import Generic, TypeVar

BM = TypeVar('BM', bound=_PydanticBaseModel)
T = TypeVar('T', bound=_PydanticBaseModel)

class AggregatePag(_PydanticBaseModel, Generic[T]):
    total: int
    data: list[T]
