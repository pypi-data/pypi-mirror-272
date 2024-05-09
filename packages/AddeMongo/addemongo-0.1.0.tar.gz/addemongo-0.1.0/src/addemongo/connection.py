from typing import Any, Optional, Sequence, Union

from addemongo._pymongo._client import AddeMongoSyncClient as _AddeMongoSyncClient
from addemongo._motor._client import AddeMongoAsyncClient as _AddeMongoAsyncClient

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
        self.host = host or "localhost"
        self.port = port or 27017
        self.tz_aware = tz_aware
        self.connect = connect
        self.kwargs = kwargs

    def async_client(
        self, database_name: str, collection_name: str, model: type[BM]
    ) -> _AddeMongoAsyncClient[BM]:
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
