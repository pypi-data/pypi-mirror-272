from typing import Any, Optional, Sequence, Union

from addemongo._motor._client import AddeMongoAsyncClient as _AddeMongoAsyncClient
from addemongo._pymongo._client import AddeMongoSyncClient as _AddeMongoSyncClient

from ._types import BM


class AddeMongoConnection:
	def __init__(
		self,
		host: Optional[Union[str, Sequence[str]]] = None,
		port: Optional[int] = None,
		tz_aware: Optional[bool] = None,
		connect: Optional[bool] = None,
		**kwargs: Any,
	) -> None:
		self.host = host
		self.port = port
		self.tz_aware = tz_aware
		self.connect = connect
		self.kwargs = kwargs

	def _ensure_host(self) -> str | Sequence[str]:
		"""
		Ensure that the host is set and return it
		else raise a ValueError
		"""
		if not self.host:
			raise ValueError("Host is required")
		return self.host

	def async_client(
		self, database_name: str, collection_name: str, model: type[BM]
	) -> _AddeMongoAsyncClient[BM]:
		"""
		Async client made with the motor package used to interact with the database
		"""
		return _AddeMongoAsyncClient[BM](
			connection=self,
			database=database_name,
			collection=collection_name,
			response_class=model,
		)

	def sync_client(
		self, database_name: str, collection_name: str, model: type[BM]
	) -> _AddeMongoSyncClient[BM]:
		return _AddeMongoSyncClient[BM](
			connection=self,
			database=database_name,
			collection=collection_name,
			response_class=model,
		)
