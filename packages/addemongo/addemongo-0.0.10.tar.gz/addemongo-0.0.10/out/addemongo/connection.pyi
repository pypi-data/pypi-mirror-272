from ._types import BM as BM
from _typeshed import Incomplete
from addemongo._motor._client import AddeMongoAsyncClient as _AddeMongoAsyncClient
from addemongo._pymongo._client import AddeMongoSyncClient as _AddeMongoSyncClient
from typing import Any, Sequence

class AddeMongoConnection:
    host: Incomplete
    port: Incomplete
    tz_aware: Incomplete
    connect: Incomplete
    kwargs: Incomplete
    def __init__(self, host: str | Sequence[str] | None = None, port: int | None = None, tz_aware: bool | None = None, connect: bool | None = None, **kwargs: Any) -> None: ...
    def async_client(self, database_name: str, collection_name: str, model: type[BM]) -> _AddeMongoAsyncClient[BM]: ...
    def sync_client(self, database_name: str, collection_name: str, model: type[BM]) -> _AddeMongoSyncClient[BM]: ...
