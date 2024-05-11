from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T', bound=BaseModel)

class Pagination(BaseModel, Generic[T]):
    data: list[T]
    pages: int
    total: int
