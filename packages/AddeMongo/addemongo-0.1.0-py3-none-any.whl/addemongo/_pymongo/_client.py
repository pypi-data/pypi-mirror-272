from math import ceil
from typing import TYPE_CHECKING, Optional

from pymongo import MongoClient as _pymongo_MongoClient

from addemongo._base_client import AddeMongoBaseClient
from addemongo.builders import AggregationBuilder, QueryBuilder
from addemongo.models.pagination import Pagination

from .._types import BM, AggregatePag, T

if TYPE_CHECKING:
    from addemongo.connection import AddeMongoConnection
    from pymongo.results import (
        DeleteResult,
        InsertManyResult,
        InsertOneResult,
        UpdateResult,
    )


class AddeMongoSyncClient(AddeMongoBaseClient[BM]):
    def __init__(
        self,
        connection: "AddeMongoConnection",
        database: str,
        collection: str,
        response_class: type[BM],
    ) -> None:
        super().__init__(connection, database, collection, response_class)
        self.client = _pymongo_MongoClient(
            host=self.connection.host,
            port=self.connection.port,
            tz_aware=self.connection.tz_aware,
            connect=self.connection.connect,
            **self.connection.kwargs,
        )
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

    def insert_one(self, document: BM) -> "InsertOneResult":
        return self.collection.insert_one(document.model_dump())

    def insert_many(self, documents: list[BM]) -> "InsertManyResult":
        return self.collection.insert_many(
            [document.model_dump() for document in documents]
        )

    def update_one(
        self, query: QueryBuilder, document: BM, upsert: bool = False
    ) -> "UpdateResult":
        return self.collection.update_one(
            filter=query.build(), update={"$set": document.model_dump()}, upsert=upsert
        )

    def update_many(
        self,
        document: BM,
        query: QueryBuilder = QueryBuilder(),
        upsert: bool = False,
    ) -> "UpdateResult":
        return self.collection.update_many(
            filter=query.build(), update={"$set": document.model_dump()}, upsert=upsert
        )

    def find_one(self, query: QueryBuilder) -> Optional[BM]:
        if document := self.collection.find_one(
            query.build(), projection=self.projection_schema()
        ):
            return self.response_class(**document)

    def find_many(
        self,
        query: QueryBuilder = QueryBuilder(),
        limit: int = 0,
        skip: int = 0,
    ) -> list[BM]:
        return [
            self.response_class(**document)
            for document in self.collection.find(
                query.build(),
                projection=self.projection_schema(),
                limit=limit,
                skip=skip,
            )
        ]

    def pagination(
        self, query: QueryBuilder = QueryBuilder(), page: int = 0, per_page: int = 10
    ) -> Pagination[BM]:
        count = self.count_documents(query)
        docs = self.find_many(
            query,
            limit=per_page,
            skip=page * per_page,
        )

        return Pagination[BM](pages=ceil(count // per_page), total=count, data=docs)

    def delete_one(self, query: QueryBuilder) -> "DeleteResult":
        return self.collection.delete_one(query.build())

    def delete_many(self, query: QueryBuilder = QueryBuilder()) -> "DeleteResult":
        return self.collection.delete_many(query.build())

    def count_documents(self, query: QueryBuilder = QueryBuilder()) -> int:
        return self.collection.count_documents(query.build())

    def aggregation(
        self,
        document_class: type[T],
        pipeline: AggregationBuilder = AggregationBuilder(),
    ) -> list[T]:
        self.collection.aggregate(pipeline=pipeline.build())
        return [
            document_class(**document)
            for document in self.collection.aggregate(pipeline=pipeline.build())
        ]

    def aggregation_pagination(
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

        for sla in raw_data:
            data = sla
            docs: AggregatePag[T] = AggregatePag(**data)
            break

        else:
            return Pagination[T](pages=0, total=0, data=[])

        return Pagination[T](
            pages=ceil(docs.total // per_page), total=docs.total, data=docs.data
        )
