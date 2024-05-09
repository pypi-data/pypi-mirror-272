from math import ceil
from typing import TYPE_CHECKING, Optional, Type

from motor.motor_asyncio import AsyncIOMotorClient as _AsyncIOMotorClient

from addemongo.models.pagination import Pagination

from .._base_client import AddeMongoBaseClient
from .._types import T, BM, AggregatePag
from ..builders import AggregationBuilder, QueryBuilder

if TYPE_CHECKING:
    from ..connection import AddeMongoConnection
    from pymongo.results import (
        InsertManyResult,
        InsertOneResult,
        UpdateResult,
        DeleteResult,
    )


class AddeMongoAsyncClient(AddeMongoBaseClient[BM]):
    def __init__(
        self,
        connection: "AddeMongoConnection",
        database: str,
        collection: str,
        response_class: Type[BM],
    ) -> None:
        super().__init__(connection, database, collection, response_class)
        self.client = _AsyncIOMotorClient(
            host=self.connection.host,
            port=self.connection.port,
            tz_aware=self.connection.tz_aware,
            connect=self.connection.connect,
            **self.connection.kwargs,
        )
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

    async def insert_one(self, document: BM) -> "InsertOneResult":
        return await self.collection.insert_one(document.model_dump())

    async def insert_many(self, documents: list[BM]) -> "InsertManyResult":
        return await self.collection.insert_many(
            [document.model_dump() for document in documents]
        )

    async def update_one(
        self, query: QueryBuilder, document: BM, upsert: bool = False
    ) -> "UpdateResult":
        return await self.collection.update_one(
            filter=query.build(), update={"$set": document.model_dump()}, upsert=upsert
        )

    async def update_many(
        self,
        document: BM,
        query: QueryBuilder = QueryBuilder(),
        upsert: bool = False,
    ) -> "UpdateResult":
        return await self.collection.update_many(
            filter=query.build(), update={"$set": document.model_dump()}, upsert=upsert
        )

    async def find_one(self, query: QueryBuilder) -> Optional[BM]:
        if document := await self.collection.find_one(
            query.build(), projection=self.projection_schema()
        ):
            return self.response_class(**document)

    async def find_many(
        self,
        query: QueryBuilder = QueryBuilder(),
        limit: int = 0,
        skip: int = 0,
    ) -> list[BM]:
        return [
            self.response_class(**document)
            for document in await self.collection.find(
                query.build(),
                projection=self.projection_schema(),
                limit=limit,
                skip=skip,
            ).to_list(length=None)
        ]

    async def delete_one(self, query: QueryBuilder) -> "DeleteResult":
        return await self.collection.delete_one(query.build())

    async def delete_many(self, query: QueryBuilder = QueryBuilder()) -> "DeleteResult":
        return await self.collection.delete_many(query.build())

    async def count_documents(self, query: QueryBuilder = QueryBuilder()) -> int:
        return await self.collection.count_documents(query.build())

    async def aggregation(
        self,
        document_class: type[T],
        pipeline: AggregationBuilder = AggregationBuilder(),
    ) -> list[T]:
        return [
            document_class(**document)
            for document in await self.collection.aggregate(
                pipeline=pipeline.build()
            ).to_list(length=None)
        ]

    async def pagination(
        self, query: QueryBuilder = QueryBuilder(), page: int = 0, per_page: int = 10
    ) -> Pagination[BM]:
        count = await self.count_documents(query)
        docs = await self.find_many(
            query,
            limit=per_page,
            skip=page * per_page,
        )

        return Pagination[BM](pages=ceil(count // per_page), total=count, data=docs)

    async def aggregation_pagination(
        self,
        document_class: type[T],
        pipeline: AggregationBuilder = AggregationBuilder(),
        page: int = 0,
        per_page: int = 10,
    ) -> Pagination[T]:

        raw_data = self.collection.aggregate(
            pipeline.set_facet(
                {
                    "total": [{"$count": "total"}],
                    "data": [
                        {
                            "$skip": page * per_page,
                        },
                        {"$limit": per_page},
                    ],
                }
            ).build()
        )

        async for data in raw_data:
            docs: AggregatePag[T] = AggregatePag(**data)
            break

        else:
            return Pagination[T](pages=0, total=0, data=[])

        return Pagination[T](
            pages=ceil(docs.total // per_page), total=docs.total, data=docs.data
        )
