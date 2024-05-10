from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Pagination(BaseModel, Generic[T]):
    data: list[T]
    pages: int
    total: int
