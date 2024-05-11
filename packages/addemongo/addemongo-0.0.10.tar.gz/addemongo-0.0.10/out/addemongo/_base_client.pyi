from ._types import BM as BM
from _typeshed import Incomplete
from addemongo.connection import AddeMongoConnection as AddeMongoConnection
from typing import Any, Generic

class AddeMongoBaseClient(Generic[BM]):
    connection: Incomplete
    database_name: Incomplete
    collection_name: Incomplete
    response_class: Incomplete
    def __init__(self, connection: AddeMongoConnection, database: str, collection: str, response_class: type[BM]) -> None: ...
    def projection_schema(self) -> dict[str, Any]: ...
